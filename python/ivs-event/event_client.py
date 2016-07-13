#!/usr/bin/python
# -*- coding: utf-8 -*-
#coding=utf-8
from __future__ import print_function
"""The Python implementation of the GRPC event.proto client."""
# import concurrent.futures
# from gevent import monkey

# monkey.patch_all()
# from gevent.threadpool import ThreadPoolExecutor
# concurrent.futures.ThreadPoolExecutor = ThreadPoolExecutor

import time
from suresecureivs_pb2 import Event
from suresecureivs_pb2 import Empty
from suresecureivs_pb2 import GeneralReply
from suresecureivs_pb2 import  EventServerAddress
from grpc.beta import implementations as beta_implementations
from grpc.beta import interfaces as beta_interfaces
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

from grpc.beta import implementations

import suresecureivs_pb2 as ss_pb2

_TIMEOUT_SECONDS = 100

def beta_create_DeviceMgt_and_EventReporting_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
  request_serializers = {
    ('suresecureivs.DeviceMgt', 'GetEventServerAddress'): Empty.SerializeToString,
    ('suresecureivs.DeviceMgt', 'GetHealthyStatus'): Empty.SerializeToString,
    ('suresecureivs.DeviceMgt', 'SetEventServerAddress'): EventServerAddress.SerializeToString,
    ('suresecureivs.EventReporting', 'ReportEvent'): Event.SerializeToString,
  }
  response_deserializers = {
    ('suresecureivs.DeviceMgt', 'GetEventServerAddress'): EventServerAddress.FromString,
    ('suresecureivs.DeviceMgt', 'GetHealthyStatus'): Empty.FromString,
    ('suresecureivs.DeviceMgt', 'SetEventServerAddress'): GeneralReply.FromString,
    ('suresecureivs.EventReporting', 'ReportEvent'): GeneralReply.FromString,
  }
  cardinalities = {
    'GetEventServerAddress': cardinality.Cardinality.UNARY_UNARY,
    'GetHealthyStatus': cardinality.Cardinality.UNARY_UNARY,
    'SetEventServerAddress': cardinality.Cardinality.UNARY_UNARY,
    'ReportEvent': cardinality.Cardinality.UNARY_UNARY,
  }
  stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
  return beta_implementations.dynamic_stub(channel, 'suresecureivs.DeviceMgt', cardinalities, options=stub_options)

import threading
class Client(threading.Thread):
    def __init__(self, threadName):
        super(Client, self).__init__(name = threadName)

    def run(self):
        channel = implementations.insecure_channel('localhost', 50051)
        stub = ss_pb2.beta_create_EventReporting_stub(channel)
        response = stub.ReportEvent(ss_pb2.Event(description='you'), _TIMEOUT_SECONDS)
        print("Greeter client received: " + response.message)


def run():
  channel = implementations.insecure_channel('localhost', 50051)
  # stub = ss_pb2.beta_create_EventReporting_stub(channel)
  stub = beta_create_DeviceMgt_and_EventReporting_stub(channel)
  # response = stub.ReportEvent(ss_pb2.Event(description='you'), _TIMEOUT_SECONDS)
  # stub = ss_pb2.beta_create_DeviceMgt_stub(channel)
  # response = stub.GetEventServerAddress.future(ss_pb2.Empty(), _TIMEOUT_SECONDS)
  responses = [stub.GetEventServerAddress.future(ss_pb2.Empty(), _TIMEOUT_SECONDS) for i in range(2000) ]
  print ("yes")
  time.sleep(2)
  print ("no")
  for res in responses:
      print(res.result())
  # print response
  # clients = []
  # for i in range(200):
    # n = Client(str(i))
    # clients.append(n)
    # n.start()
  # for c in clients:
      # c.join()
  # channel = implementations.insecure_channel('localhost', 50051)
  # stub = ss_pb2.beta_create_EventReporting_stub(channel)
  # response = stub.ReportEvent(ss_pb2.Event(description='you'), _TIMEOUT_SECONDS)
  # print("Greeter client received: " + response.message)


if __name__ == '__main__':
  run()
