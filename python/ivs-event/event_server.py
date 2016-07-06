
"""The Python implementation of the GRPC helloworld.Greeter server."""

import time

import event_pb2
import tasks

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class EventReporting(event_pb2.BetaEventReportingServicer):

  def ReportEvent(self, request, context):
    # res = tasks.add.delay(1,2)
    res = tasks.fall_event.delay(request)
    result = res.get()
    # return event_pb2.ReportEventReply(message='Hello, %s %d!' % request.description, result)
    return event_pb2.ReportEventReply(message='Hello, %s!' % result)

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
