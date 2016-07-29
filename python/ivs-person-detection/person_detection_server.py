
"""The Python implementation of the GRPC helloworld.Greeter server."""

import time

import suresecureivs_pb2 as ss_pb2
import tasks
import celery
import matplotlib.pyplot as plt
import cStringIO as StringIO
import numpy as np
import caffe

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ImageAnalysis(ss_pb2.BetaImageAnalysisServicer):

  def ObjectDetection(self, request, context):
    # string_buffer = StringIO.StringIO(request.img)
    # img = caffe.io.load_image(string_buffer)
    # plt.figure()
    # plt.imshow(img)
    # plt.show()
    # res = tasks.ImageClassify.delay(request, expires=1)
    try:
      res = tasks.ObjectDetection.apply_async(args=[request], expires=5)
      result = res.get()
      reply = ss_pb2.ObjectDetectionReply()
      for r in result:
          new_target = reply.targets.add()
          new_target.x = r[0]
          new_target.y = r[1]
          new_target.w = r[2]
          new_target.h = r[3]
          new_target.type = ss_pb2.OBJECT_TYPE_PERSON
      print(result)
      reply.general_reply = ss_pb2.GeneralReply(error_code = 0)
      return reply
    except celery.exceptions.TaskRevokedError:
      general_reply = ss_pb2.GeneralReply(error_code = 10, message = "server is too busy")
      return ss_pb2.ObjectDetectionReply(general_reply=general_reply)

def serve():
  img_region = ss_pb2.ImageRegion()
  img_file = open("/home/mythxcq/3.jpg", "rb")
  img_region.img = img_file.read()
  img_file.close()
  print("test add")
  res = tasks.ObjectDetection.apply_async(args=[img_region], expires=1)
  dets = res.get()
  print(dets)
  # for i in inds:
      # bbox = dets[i, :4]
      # score = dets[i, -1]
      # cv2.rectangle(im, (bbox[0],bbox[1]), (bbox[2],bbox[3]),
                    # (255,0,0), 2)
      # cv2.putText(im, str(score), (bbox[0], bbox[3]), cv2.FONT_HERSHEY_SIMPLEX,
                    # 1, (255,0,0))

  # res = tasks.TestAdd.apply_async([1,2], expires=1)
  # res2 = tasks.TestAdd.apply_async([1,2], expires=1)
  # print(res.get())
  # print(res2.get())

  # server = ss_pb2.beta_create_ImageAnalysis_server(ImageAnalysis(), pool_size=2000)
  # server.add_insecure_port('[::]:50051')
  # server.start()
  # try:
    # while True:
      # time.sleep(_ONE_DAY_IN_SECONDS)
  # except KeyboardInterrupt:
    # server.stop(0)

if __name__ == '__main__':
  serve()
