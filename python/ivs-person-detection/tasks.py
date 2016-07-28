from __future__ import absolute_import
import suresecureivs_pb2 as ss_pb2
import numpy as np
import os
from os import path, environ
import optparse
import settings
import celery
import logging
import time
import _init_paths
os.environ['GLOG_minloglevel'] = '2'
# import caffe
import cStringIO as StringIO
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from utils.timer import Timer
import scipy.io as sio
import caffe, os, sys
import argparse
print __name__

the_celery = celery.Celery('tasks')
                # broker=CELERY_BROKER_URL,
                # backend=CELERY_RESULT_BACKEND)
the_celery.config_from_object(settings)

# print the_celery
# print app.config['CELERYD_POOL']

prototxt = "/home/mythxcq/caffe_person_classification_models/google_net/deploy_112.prototxt"
caffemodel = "/home/mythxcq/caffe_person_classification_models/google_net/finetune_person_googlenet_112.caffemodel"

cfg.TEST.HAS_RPN = True  # Use RPN for proposals
cfg.TEST.BBOX_REG = False

# args = parse_args()

# prototxt = os.path.join(cfg.MODELS_DIR, NETS[args.demo_net][0],
                        # 'faster_rcnn_alt_opt', 'faster_rcnn_test.pt')
# caffemodel = os.path.join(cfg.DATA_DIR, 'faster_rcnn_models',
                          # NETS[args.demo_net][1])

# if not os.path.isfile(caffemodel):
    # raise IOError(('{:s} not found.\nDid you run ./data/script/'
                   # 'fetch_faster_rcnn_models.sh?').format(caffemodel))

# if args.cpu_mode:
caffe.set_mode_cpu()
# else:
    # caffe.set_mode_gpu()
    # caffe.set_device(args.gpu_id)
    # cfg.GPU_ID = args.gpu_id
net = caffe.Net(prototxt, caffemodel, caffe.TEST)
# classifier = 0
# print "get batch size"
# caffe.set_mode_cpu()
# classifier = caffe.Classifier(model_def, pretrained_model)
# batch_size = classifier.blobs[classifier.inputs[0]].data.shape[0]
# classifier = None
# batch_size = 1

from celery.signals import worker_process_init
from celery.signals import worker_init
from billiard import current_process
import time
@worker_init.connect
def init_workers(sender, signal):
    print "init workers"
    # batch_size = 5
@worker_process_init.connect
def configure_workers(sender, signal):
    # print "worker init" + str(os.getpid())
    # Make classifier.
    # model_def = "/home/mythxcq/caffe_person_classification_models/google_net/deploy_112.prototxt"
    # pretrained_model = "/home/mythxcq/caffe_person_classification_models/google_net/finetune_person_googlenet_112.caffemodel"
    # caffe.set_mode_gpu()
    # caffe.set_device(current_process().index)
    global person_detection_net
    person_detection_net = caffe.Net(prototxt, caffemodel, caffe.TEST)
    # global classifier
    mean = np.array([104,117,123])
    # classifier = caffe.Classifier(model_def, pretrained_model,
            # mean=mean, input_scale=None, raw_scale=255.0)
    # classifier.index = current_process().index
    # print current_process().index
    # print classifier
            # mean=mean)

# @the_celery.task(name="tasks.ImageClassify")
# def ImageClassify(image_region):
    # string_buffer = StringIO.StringIO(image_region.img)
    # image = caffe.io.load_image(string_buffer)
    # inputs = [image]
    # predictions = classifier.predict(inputs, False)
    # print predictions
    # if(np.argmax(predictions[0]) == 0):
        # return image_analysis_pb2.ImageClassifyReply.PERSON
    # else:
        # return image_analysis_pb2.ImageClassifyReply.BACK_GROUND
    # print current_process().index
    # time.sleep(2)

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
    logger.info ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    # CONF_THRESH = 0.0

    CONF_THRESH = 0.8
    NMS_THRESH = 0.3
    person_idx = CLASSES.index('person')
    person_boxes = boxes[:, 4*person_idx:4*(person_idx + 1)]
    person_scores = scores[:, person_idx]
    person_dets = np.hstack((person_boxes,
                      person_scores[:, np.newaxis])).astype(np.float32)
    person_keep = nms(person_dets, NMS_THRESH)
    person_dets = person_dets[person_keep, :]
    return person_dets
    # CONF_THRESH = 0.8
    # vis_person_detections(im, person_dets, thresh=CONF_THRESH)

@the_celery.task(name="tasks.ObjectDetection", queue="important")
def ObjectDetection(imgreg):
    # img_str = StringIO.StringIO(imgreg.img)
    # img = caffe.io.load_image(img_str)
    # input_img = img[ireg.y:ireg.y+ireg.h,ireg.x:ireg.x+ireg.w,:] if ireg.w>0 and ireg.h>0 else img
    # detect_img(person_detection_net, input_img)
    # general_reply = ss_pb2.GeneralReply(error_code = 0)
    person_dets = []
    return person_dets

# import batches
# @the_celery.task(name="tasks.BatchPersonDetection", queue="important", base=batches.Batches, flush_every=batch_size, flush_interval=1)
# def ImageClassify(requests):
    # print len(requests)
    # # print current_process().index
    # # print classifier
    # # print classifier.index
    # # print "batch size"
    # # print batch_size
    # time.sleep(2)
    # img_regions = [request.args[0] for request in requests]
    # img_strings = [StringIO.StringIO(ireg.img) for ireg in img_regions]
    # imgs = [caffe.io.load_image(sbuf) for sbuf in img_strings]
    # inputs = [img[ireg.y:ireg.y+ireg.h,ireg.x:ireg.x+ireg.w,:] if ireg.w>0 and ireg.h>0 else img for img,ireg in zip(imgs,img_regions)]

    # predictions = classifier.predict(inputs, False)
    # # print predictions
    # # print predictions.argmax(1)
    # responses = [ss_pb2.ImageClassifyReply.PERSON if predmax == 0 else ss_pb2.ImageClassifyReply.BACK_GROUND
                 # for predmax in predictions.argmax(1)]
    # # print responses

    # # responses = [request.args[0]+request.args[1] for request in requests]
    # # for request in requests:
        # # print request.__dict__
        # # print request.args[0]
        # # print request.args[1]
    # # print the_celery
    # for response, request in zip(responses, requests):
        # the_celery.backend.mark_as_done(request.id, response)
        # # print 'mark as done'

if __name__ == '__main__':
    celery()
