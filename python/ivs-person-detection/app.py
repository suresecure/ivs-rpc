# from __future__ import absolute_import
import flask
import werkzeug
import celery
import celery.exceptions
import os
import logging
# import batches
import time
import datetime
import flask_restful
# import tasks

app = flask.Flask(__name__)

import settings
the_celery = celery.Celery('tasks')
the_celery.config_from_object(settings)
@the_celery.task(name="tasks.ObjectDetection", queue="important")
def ObjectDetection(imgstream, secure_filename):
    pass

# class ImageManagement(restful.Resource):
    # def post(self):
        # pass

# curl -X POST -F image=@hy0.jpg http://localhost:8000/person_detection
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

        # img_region = ss_pb2.ImageRegion()

        imagefile = flask.request.files['image']
        imagestream = imagefile.read()
        # img_region.img = imagefile.read()

        filename_ = str(datetime.datetime.now()).replace(' ', '_') + \
            werkzeug.secure_filename(imagefile.filename)

        try:
          # res = tasks.ObjectDetection.apply_async(args=[imagestream, filename_], expires=5)
          res = ObjectDetection.apply_async(args=[imagestream, filename_], expires=5)
          result = res.get()
          print(result)
        except celery.exceptions.TaskRevokedError:
          return {'error': 'time is out'}
        except AttributeError:
          return {'error': 'iamge is invalid'}
        # targets = [{'x':1,'y':2,'w':3,'h':4}]
        return {'targets':result}

api = flask_restful.Api(app)
api.add_resource(PersonDetection, '/person_detection')

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    # start_from_terminal(app)
    app.run(debug=True, threaded=True, host='0.0.0.0', port=8000)

# start celery workers
# celery -A app.the_celery worker
# start with gunicorn and gevent
# gunicorn -k=gevent app:app -b 0.0.0.0
