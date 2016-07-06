from __future__ import absolute_import
import event_pb2
import numpy as np
from os import path, environ
# import json
# from flask import Flask, Blueprint, abort, jsonify, request, session
# import flask
import optparse
import settings
# import tornado.wsgi
# import tornado.httpserver
import celery
import logging
# import batches
import time
# import _init_paths
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
    # caffe.set_device(0)
    print current_process().index
    print "worker init" + str(os.getpid())

import os
@the_celery.task(name="tasks.fall_event")
def fall_event(evt):
    print current_process().index
    print evt.description
    # time.sleep(2)
    return evt.description
# @the_celery.task(name="tasks.add")
# def add(x, y):
    # print current_process().index
    # # time.sleep(2)
    # return x + y
import celery.contrib.batches
@the_celery.task(name="tasks.add", base=celery.contrib.batches.Batches, flush_every=4, flush_interval=2)
def add(requests):
    print len(requests)
    print os.getpid()
    # print self.__dict__
    # print requests.__dict__
    responses = [request.args[0]+request.args[1] for request in requests]
    for request in requests:
        print request.__dict__
        # print request.args[0]
        # print request.args[1]
    print the_celery
    for response, request in zip(responses, requests):
        print 'mark as done'
        the_celery.backend.mark_as_done(request.id, response)

if __name__ == '__main__':
    celery()
