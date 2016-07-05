
"""The Python implementation of the GRPC helloworld.Greeter server."""

import time

import image_analysis_pb2
import tasks

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ImageAnalysis(image_analysis_pb2.BetaImageAnalysisServicer):

  def ImageClassify(self, request, context):
    res = tasks.ImageClassify.delay(request)
    result = res.get()
    return image_analysis_pb2.ImageClassifyReply(type=result)
    # return im_pb2.ReportEventReply(message='Hello, %s %d!' % request.description, result)
    # print request.x
    # print request.y

def serve():
  server = image_analysis_pb2.beta_create_ImageAnalysis_server(ImageAnalysis())
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
