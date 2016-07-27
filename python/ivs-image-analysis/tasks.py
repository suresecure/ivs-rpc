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
import caffe
import cStringIO as StringIO
# from fast_rcnn.config import cfg
# from fast_rcnn.test import im_detect
# from fast_rcnn.nms_wrapper import nms
# from utils.timer import Timer
# import scipy.io as sio
# import caffe, os, sys, cv2
import argparse
print __name__

the_celery = celery.Celery('tasks')
                # broker=CELERY_BROKER_URL,
                # backend=CELERY_RESULT_BACKEND)
the_celery.config_from_object(settings)

# print the_celery
# print app.config['CELERYD_POOL']

model_def = "/home/mythxcq/caffe_person_classification_models/google_net/deploy_112.prototxt"
pretrained_model = "/home/mythxcq/caffe_person_classification_models/google_net/finetune_person_googlenet_112.caffemodel"
# classifier = 0
print "get batch size"
caffe.set_mode_cpu()
classifier = caffe.Classifier(model_def, pretrained_model)
batch_size = classifier.blobs[classifier.inputs[0]].data.shape[0]
classifier = None
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
    global classifier
    mean = np.array([104,117,123])
    classifier = caffe.Classifier(model_def, pretrained_model,
            mean=mean, input_scale=None, raw_scale=255.0)
    classifier.index = current_process().index
    print current_process().index
    print classifier
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

@the_celery.task(name="tasks.TestAdd", queue="important")
def TestAdd(a, b):
    print(a)
    print(b)
    time.sleep(5)
    return a+b

import batches
@the_celery.task(name="tasks.ImageClassify", queue="important", base=batches.Batches, flush_every=batch_size, flush_interval=1)
def ImageClassify(requests):
    print len(requests)
    # print current_process().index
    # print classifier
    # print classifier.index
    # print "batch size"
    # print batch_size
    time.sleep(2)
    img_regions = [request.args[0] for request in requests]
    img_strings = [StringIO.StringIO(ireg.img) for ireg in img_regions]
    imgs = [caffe.io.load_image(sbuf) for sbuf in img_strings]
    inputs = [img[ireg.y:ireg.y+ireg.h,ireg.x:ireg.x+ireg.w,:] if ireg.w>0 and ireg.h>0 else img for img,ireg in zip(imgs,img_regions)]

    predictions = classifier.predict(inputs, False)
    # print predictions
    # print predictions.argmax(1)
    responses = [ss_pb2.ImageClassifyReply.PERSON if predmax == 0 else ss_pb2.ImageClassifyReply.BACK_GROUND
                 for predmax in predictions.argmax(1)]
    # print responses

    # responses = [request.args[0]+request.args[1] for request in requests]
    # for request in requests:
        # print request.__dict__
        # print request.args[0]
        # print request.args[1]
    # print the_celery
    for response, request in zip(responses, requests):
        the_celery.backend.mark_as_done(request.id, response)
        # print 'mark as done'

if __name__ == '__main__':
    celery()
