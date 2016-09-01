# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Set up paths for Fast R-CNN."""

import os.path as osp
import sys

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)

this_dir = osp.dirname(__file__)

# Add caffe to PYTHONPATH
# caffe_path = osp.join(this_dir, '..', 'caffe-fast-rcnn', 'python')
# caffe_path = "/home/mythxcq/source_codes/faster_rcnn/py-faster-rcnn/caffe-fast-rcnn/python"
caffe_path = "/home/mythxcq/work/faster_rcnn/py-faster-rcnn/caffe-fast-rcnn/python"
add_path(caffe_path)

# Add lib to PYTHONPATH
# lib_path = osp.join(this_dir, '..', 'lib')
lib_path = "/home/mythxcq/work/faster_rcnn/py-faster-rcnn/lib"
add_path(lib_path)
