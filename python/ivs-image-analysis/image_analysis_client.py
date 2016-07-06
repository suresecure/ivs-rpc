
"""The Python implementation of the GRPC event.proto client."""

from __future__ import print_function

from grpc.beta import implementations

import image_analysis_pb2

_TIMEOUT_SECONDS = 10


def run():
  channel = implementations.insecure_channel('localhost', 50051)
  stub = image_analysis_pb2.beta_create_ImageAnalysis_stub(channel)
  img_region = image_analysis_pb2.ImageRegion()
  # img_file = open("/home/mythxcq/source_codes/caffe/examples/images/cat.jpg", "rb")
  img_file = open("/home/mythxcq/1.jpg", "rb")
  img_region.img = img_file.read()
  img_file.close()
  response = stub.ImageClassify(img_region, _TIMEOUT_SECONDS)
  print("Greeter client received: %d" % response.type)


if __name__ == '__main__':
  run()
