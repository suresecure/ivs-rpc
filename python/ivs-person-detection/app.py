from __future__ import absolute_import
from os import path, environ
import json
from flask import Flask, Blueprint, abort, jsonify, request, session
import flask
import werkzeug
# import optparse
# import settings
# import tornado.wsgi
# import tornado.httpserver
import celery
import os
import logging
# import batches
import time
import datetime
import flask_restful
# from flask.ext import restful
# import tasks
import suresecureivs_pb2 as ss_pb2
UPLOAD_FOLDER = '/tmp/caffe_demos_uploads'

app = Flask(__name__)
# app.config.from_object(settings)

# class ImageManagement(restful.Resource):
    # def post(self):
        # pass

# curl -X POST -F image=@hy0.jpg http://localhost:8000
class PersonDetection(flask_restful.Resource):
    def post(self):
        # import pdb; pdb.set_trace()  # XXX BREAKPOINT
        # print request.json
        # print request.data
        # x = int(request.args.get("x", x))
        # y = int(request.args.get("y", y))
        # print request.json
        # time.sleep(10)
        # url = request.json['url']
        # x = request.json['x']
        # y = request.json['y']
        # h = request.json['h']
        # w = request.json['w']
        # res = add.apply_async((x, y))

        print flask.request
        print len(flask.request.files)

        imagefile = flask.request.files['image']
        filename_ = str(datetime.datetime.now()).replace(' ', '_') + \
            werkzeug.secure_filename(imagefile.filename)
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        imagefile.save(filename)

        img_region = ss_pb2.ImageRegion()
        img_region.img = imagefile

        reply = ss_pb2.ObjectDetectionReply()
        try:
          res = tasks.ObjectDetection.apply_async(args=[img_region], expires=5)
          result = res.get()
          targets = []
          for r in result:
              x = (int)(r[0].item())
              y = (int)(r[1].item())
              w = (int)(r[2].item())-new_target.x
              h = (int)(r[3].item())-new_target.y
              targets.append({'x':x,'y':y,'w':w,'h':h})
          print(targets)
        except celery.exceptions.TaskRevokedError:
          return {'error': 'time is out'}
        except AttributeError:
          return {'error': 'iamge is invalid'}
        # targets = [{'x':1,'y':2,'w':3,'h':4}]
        return {'targets':targets}

        # context = {"id": res.task_id, "x": x, "y": y}
        # result = "add((x){}, (y){})".format(context['x'], context['y'])
        # goto = "{}".format(context['id'])
        # # return jsonify(result=result, goto=goto)
        # return {'result':result, 'goto':goto}
    # def get(self):
        # task_id = request.args.get("task_id")
        # result = add.AsyncResult(task_id)
        # # print result.ready()
        # # retval = result.get(timeout=1.0)
        # retval = result.get()
        # # if result.ready():
            # # return {'result':result.get()}
        # # else:
            # # return {'result':-1}
        # return {'result':retval}
        # # # print retval

api = flask_restful.Api(app)
api.add_resource(PersonDetection, '/person_detection')

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    # start_from_terminal(app)
    app.run(debug=True, threaded=True, host='0.0.0.0', port=8000)

# start celery workers
# celery -A app.the_celery worker
# start with gunicorn and gevent
# gunicorn -k=gevent app:app
