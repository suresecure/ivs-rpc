from __future__ import absolute_import
import image_analysis_pb2
import numpy as np
import os
from os import path, environ
import optparse
import settings
import celery
import logging
import time
import _init_paths
import caffe
import cStringIO as StringIO
# from fast_rcnn.config import cfg
# from fast_rcnn.test import im_detect
# from fast_rcnn.nms_wrapper import nms
# from utils.timer import Timer
# import scipy.io as sio
# import caffe, os, sys, cv2
import argparse

# the_celery = make_celery(app)
# SECRET_KEY = 'not_a_secret'
# CELERY_BROKER_URL='redis://localhost:6379/0'
# CELERY_RESULT_BACKEND='redis://localhost:6379/0'

# CELERY_BROKER_URL='amqp://guest:guest@localhost:5672//'
# CELERY_RESULT_BACKEND='amqp://guest:guest@localhost:5672//'
# CELERYD_CONCURRENCY = 4
# CELERYD_PREFETCH_MULTIPLIER = 0
the_celery = celery.Celery('tasks')
                # broker=CELERY_BROKER_URL,
                # backend=CELERY_RESULT_BACKEND)
the_celery.config_from_object(settings)

# print the_celery
# print app.config['CELERYD_POOL']

from celery.signals import worker_process_init
from billiard import current_process
import time
@worker_process_init.connect
def configure_workers(sender, signal):
    # print signal.__dict__
    # print sender
    # time.sleep(10)
    # caffe.set_mode_gpu()
    print current_process().index
    # caffe.set_device(current_process().index)
    # print "worker init" + str(os.getpid())
    # Make classifier.
    model_def = "/home/mythxcq/caffe_person_classification_models/google_net/deploy_112.prototxt"
    pretrained_model = "/home/mythxcq/caffe_person_classification_models/google_net/finetune_person_googlenet_112.caffemodel"
    # mean_file = ""
    # mean = np.load(mean_file)
    mean = np.empty((3,112,112),dtype=np.float32)
    mean[0] = 104
    mean[1] = 117
    mean[2] = 123
    global classifier
    classifier = caffe.Classifier(model_def, pretrained_model,
            mean=mean)

@the_celery.task(name="tasks.ImageClassify")
def ImageClassify(image_region):
    string_buffer = StringIO.StringIO(image_region.img)
    image = caffe.io.load_image(string_buffer)
    inputs = [image]
    predictions = classifier.predict(inputs, False)
    print predictions
    if predictions[0][1] > 0.8:
        return image_analysis_pb2.ImageClassifyReply.PERSON
    else:
        return image_analysis_pb2.ImageClassifyReply.BACK_GROUND
    # print current_process().index
    # time.sleep(2)

# import celery.contrib.batches
# @the_celery.task(name="tasks.add", base=celery.contrib.batches.Batches, flush_every=4, flush_interval=2)
# def add(requests):
    # print len(requests)
    # print os.getpid()
    # # print self.__dict__
    # # print requests.__dict__
    # responses = [request.args[0]+request.args[1] for request in requests]
    # for request in requests:
        # print request.__dict__
        # # print request.args[0]
        # # print request.args[1]
    # print the_celery
    # for response, request in zip(responses, requests):
        # print 'mark as done'
        # the_celery.backend.mark_as_done(request.id, response)

if __name__ == '__main__':
    celery()
