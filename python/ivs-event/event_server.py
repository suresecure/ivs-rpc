
"""The Python implementation of the GRPC helloworld.Greeter server."""
# import concurrent.futures
# from gevent import monkey

# monkey.patch_all()
# from gevent.threadpool import ThreadPoolExecutor
# concurrent.futures.ThreadPoolExecutor = ThreadPoolExecutor

import time

import suresecureivs_pb2 as ss_pb2
from suresecureivs_pb2 import Event
from suresecureivs_pb2 import Empty
from suresecureivs_pb2 import GeneralReply
from suresecureivs_pb2 import  EventServerAddress
from grpc.beta import implementations as beta_implementations
from grpc.beta import interfaces as beta_interfaces
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities
# import tasks
import threading

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def beta_create_DeviceMgt_and_EventReporting_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
  request_deserializers = {
    ('suresecureivs.DeviceMgt', 'GetEventServerAddress'): Empty.FromString,
    ('suresecureivs.DeviceMgt', 'GetHealthyStatus'): Empty.FromString,
    ('suresecureivs.DeviceMgt', 'SetEventServerAddress'): EventServerAddress.FromString,
    ('suresecureivs.EventReporting', 'ReportEvent'): Event.FromString,
  }
  response_serializers = {
    ('suresecureivs.DeviceMgt', 'GetEventServerAddress'): EventServerAddress.SerializeToString,
    ('suresecureivs.DeviceMgt', 'GetHealthyStatus'): Empty.SerializeToString,
    ('suresecureivs.DeviceMgt', 'SetEventServerAddress'): GeneralReply.SerializeToString,
    ('suresecureivs.EventReporting', 'ReportEvent'): GeneralReply.SerializeToString,
  }
  method_implementations = {
    ('suresecureivs.DeviceMgt', 'GetEventServerAddress'): face_utilities.unary_unary_inline(servicer.GetEventServerAddress),
    ('suresecureivs.DeviceMgt', 'GetHealthyStatus'): face_utilities.unary_unary_inline(servicer.GetHealthyStatus),
    ('suresecureivs.DeviceMgt', 'SetEventServerAddress'): face_utilities.unary_unary_inline(servicer.SetEventServerAddress),
    ('suresecureivs.EventReporting', 'ReportEvent'): face_utilities.unary_unary_inline(servicer.ReportEvent),
  }
  server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
  return beta_implementations.server(method_implementations, options=server_options)

class EventReporting(ss_pb2.BetaEventReportingServicer, ss_pb2.BetaDeviceMgtServicer):

  def ReportEvent(self, request, context):
    print threading.current_thread()
    # time.sleep(2)
    # gevent.sleep(2)
    # res = tasks.add.delay(1,2)
    # res = tasks.fall_event.delay(request)
    # result = res.get()
    # return ss_pb2.ReportEventReply(message='Hello, %s %d!' % request.description, result)
    return ss_pb2.GeneralReply(message='Hello, %s!' % "yes")
  def GetHealthyStatus(self, request, context):
    return ss_pb2.Empty()
  def GetEventServerAddress(self, request, context):
    print "Get Event Server Address"
    time.sleep(2)
    return ss_pb2.EventServerAddress(address = "123")
  def SetEventServerAddress(self, request, context):
    return ss_pb2.GeneralReply(message='Hello, %s!' % "yes")

def serve():
  # server = ss_pb2.beta_create_EventReporting_server(EventReporting())
  server = beta_create_DeviceMgt_and_EventReporting_server(EventReporting(), pool_size=2000)
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
