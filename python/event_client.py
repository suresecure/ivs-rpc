
"""The Python implementation of the GRPC event.proto client."""

from __future__ import print_function

from grpc.beta import implementations

import event_pb2

_TIMEOUT_SECONDS = 10


def run():
  channel = implementations.insecure_channel('localhost', 50051)
  stub = event_pb2.beta_create_EventReporting_stub(channel)
  response = stub.ReportEvent(event_pb2.Event(description='you'), _TIMEOUT_SECONDS)
  print("Greeter client received: " + response.message)


if __name__ == '__main__':
  run()
