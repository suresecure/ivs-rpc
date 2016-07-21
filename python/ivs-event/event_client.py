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
from suresecureivs_pb2 import  NetworkEndpoint
from grpc.beta import implementations as beta_implementations
from grpc.beta import interfaces as beta_interfaces
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

from grpc.beta import implementations

import suresecureivs_pb2 as ss_pb2

_TIMEOUT_SECONDS = 100


def run():
  channel = implementations.insecure_channel('localhost', 50051)
  event_reporting_stub = ss_pb2.beta_create_EventReporting_stub(channel)
  # stub = beta_create_DeviceMgt_and_EventReporting_stub(channel)
  response = event_reporting_stub.ReportEvent(ss_pb2.Event(description='you'), _TIMEOUT_SECONDS)
  # print(response)
  # device_mgt_stub = ss_pb2.beta_create_DeviceMgt_stub(channel)
  # response = device_mgt_stub.GetEventServerAddress(ss_pb2.Empty(), _TIMEOUT_SECONDS);
  print(response)

  # response = stub.GetEventServerAddress.future(ss_pb2.Empty(), _TIMEOUT_SECONDS)
  # responses = [stub.GetEventServerAddress.future(ss_pb2.Empty(), _TIMEOUT_SECONDS) for i in range(2000) ]
  # print ("yes")
  # time.sleep(2)
  # print ("no")
  # for res in responses:
      # print(res.result())
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
