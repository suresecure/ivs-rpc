
"""The Python implementation of the GRPC event.proto client."""

from __future__ import print_function

from grpc.beta import implementations
import cStringIO as StringIO
import _init_paths
import numpy as np
import caffe

import suresecureivs_pb2 as ss_pb2

_TIMEOUT_SECONDS = 500


def run():
  channel = implementations.insecure_channel('localhost', 50051)
  stub = ss_pb2.beta_create_ImageAnalysis_stub(channel)
  img_region = ss_pb2.ImageRegion()
  # img_file = open("/home/mythxcq/source_codes/caffe/examples/images/cat.jpg", "rb")
  img_file = open("/home/mythxcq/2.jpg", "rb")
  img_region.img = img_file.read()
  # img_region.x = 0
  # img_region.w = 1000
  # img_region.y = 0
  # img_region.h = 1000
  img_file.close()
  # string_buffer = StringIO.StringIO(img_region.img)
  # img = caffe.io.load_image(string_buffer)
  # inputs = [img]
  # model_def = "/home/mythxcq/caffe_person_classification_models/google_net/deploy_112.prototxt"
  # pretrained_model = "/home/mythxcq/caffe_person_classification_models/google_net/finetune_person_googlenet_112.caffemodel"
  # mean_file = ""
  # mean = np.load(mean_file)
  # mean = np.empty((3,112,112),dtype=np.float32)
  # mean[0] = 104
  # mean[1] = 117
  # mean[2] = 123
  # global classifier
  # mean = np.array([104,117,123])
  # classifier = caffe.Classifier(model_def, pretrained_model)
  # predictions = classifier.predict(inputs, False)
  # print(predictions)

  response = [stub.ImageClassify.future(img_region, _TIMEOUT_SECONDS) for i in range(5) ]

  print("send all tasks")

  for res in response:
      print(res.result().type)
  # response = [res.result() for res in response]
  # print("Greeter client received: %d" % response.type)
  # print("Greeter client received1: %d" % response1.type)


if __name__ == '__main__':
    run()
