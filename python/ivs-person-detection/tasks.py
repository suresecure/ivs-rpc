import os
import optparse
import settings
import celery
import logging
import time
import config

the_celery = celery.Celery('tasks')
the_celery.config_from_object(settings)

import _init_paths
from utils.timer import Timer
os.environ['GLOG_minloglevel'] = '2'
import numpy as np
import cv2
import caffe
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms

def init_net(index):
    prototxt = config.prototxt
    caffemodel = config.caffemodel

    cfg.TEST.HAS_RPN = True  # Use RPN for proposals
    cfg.TEST.BBOX_REG = False
    caffe.set_mode_gpu()
    # index = 1
    print "device index:"+str(index)
    caffe.set_device(index)
    cfg.GPU_ID = index
    global person_detection_net
    person_detection_net = caffe.Net(prototxt, caffemodel, caffe.TEST)

from celery.signals import worker_process_init
from celery.signals import worker_init
from billiard import current_process
@worker_init.connect
def init_workers(sender, signal):
    print "init workers"
    # batch_size = 5
@worker_process_init.connect
def configure_workers(sender, signal):
    init_net(current_process().index)

CLASSES = ('__background__',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor')

def detect_image(net, im):
    """Detect object classes in an image using pre-computed object proposals."""

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(net, im)
    timer.toc()
    print(str(current_process().index)+' Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    # CONF_THRESH = 0.0

    CONF_THRESH = 0.4
    NMS_THRESH = 0.1
    person_idx = CLASSES.index('person')
    person_boxes = boxes[:, 4*person_idx:4*(person_idx + 1)]
    person_scores = scores[:, person_idx]
    person_dets = np.hstack((person_boxes,
                      person_scores[:, np.newaxis])).astype(np.float32)
    person_keep = nms(person_dets, NMS_THRESH)
    person_dets = person_dets[person_keep, :]
    # inds = np.where(dets[:, -1] >= CONF_THRESH)[0]
    person_dets = person_dets[np.where(person_dets[:, -1] >= CONF_THRESH)]
    return person_dets
    # CONF_THRESH = 0.8
    # vis_person_detections(im, person_dets, thresh=CONF_THRESH)

@the_celery.task(name="tasks.ObjectDetection", queue="important")
def ObjectDetection(imgstream, secure_filename):

    targets = []
    img = cv2.imdecode(np.asarray(bytearray(imgstream), dtype=np.uint8), -1)
    result = detect_image(person_detection_net, img)

    for r in result:
        x = (int)(r[0].item())
        y = (int)(r[1].item())
        w = (int)(r[2].item())-x
        h = (int)(r[3].item())-y
        targets.append({'x':x,'y':y,'w':w,'h':h})

    return targets
