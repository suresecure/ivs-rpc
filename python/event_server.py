
"""The Python implementation of the GRPC helloworld.Greeter server."""

import time

import event_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class EventReporting(event_pb2.BetaEventReportingServicer):

  def ReportEvent(self, request, context):
    return event_pb2.ReportEventReply(message='Hello, %s!' % request.description)

def serve():
  server = event_pb2.beta_create_EventReporting_server(EventReporting())
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
