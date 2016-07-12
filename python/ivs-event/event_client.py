#!/usr/bin/python
# -*- coding: utf-8 -*-
#coding=utf-8
"""The Python implementation of the GRPC event.proto client."""

from __future__ import print_function

from grpc.beta import implementations

import suresecureivs_pb2 as ss_pb2

_TIMEOUT_SECONDS = 20

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
  clients = []
  for i in range(300):
    n = Client(str(i))
    clients.append(n)
    n.start()
  for c in clients:
      c.join()
  # channel = implementations.insecure_channel('localhost', 50051)
  # stub = ss_pb2.beta_create_EventReporting_stub(channel)
  # response = stub.ReportEvent(ss_pb2.Event(description='you'), _TIMEOUT_SECONDS)
  # print("Greeter client received: " + response.message)


if __name__ == '__main__':
  run()
