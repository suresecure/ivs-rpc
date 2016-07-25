
"""The Python implementation of the GRPC helloworld.Greeter server."""

import time

import suresecureivs_pb2 as ss_pb2
import tasks
import matplotlib.pyplot as plt
import cStringIO as StringIO
import numpy as np
import caffe

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ImageAnalysis(ss_pb2.BetaImageAnalysisServicer):

  def ImageClassify(self, request, context):
    # string_buffer = StringIO.StringIO(request.img)
    # img = caffe.io.load_image(string_buffer)
    # plt.figure()
    # plt.imshow(img)
    # plt.show()
    print("new task")
    # res = tasks.ImageClassify.delay(request, expires=1)
    res = tasks.ImageClassify.apply_async(args=[request], expires=1)
    result = res.get()
    return ss_pb2.ImageClassifyReply(type=result)

def serve():
  server = ss_pb2.beta_create_ImageAnalysis_server(ImageAnalysis(), pool_size=2000)
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
