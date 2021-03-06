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
import config

if not os.path.exists(config.UPLOAD_FOLDER):
    os.makedirs(config.UPLOAD_FOLDER)
if not os.path.exists(config.UPLOAD_FOLDER_DETECTED):
    os.makedirs(config.UPLOAD_FOLDER_DETECTED)

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

num_complete_requests = 0

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

        # print flask.request
        try:
          # print len(flask.request.files)
          imagefile = flask.request.files['image']
          imagestream = imagefile.read()

          filename_ = str(datetime.datetime.now()).replace(' ', '_') + \
              werkzeug.secure_filename(imagefile.filename)

          res = ObjectDetection.apply_async(args=[imagestream, filename_], expires=5)

          filename = os.path.join(config.UPLOAD_FOLDER, filename_)
          with open(filename, "wb") as f:
              f.write(imagestream)

          result = res.get()
          if len(result)>0:
              filename = os.path.join(config.UPLOAD_FOLDER_DETECTED, filename_)
              with open(filename, 'w') as f:
                  f.write(str(result))
          num_complete_requests += 1
          return {'targets':result}
        except celery.exceptions.TaskRevokedError:
          print('time is out')
          return {'error': 'time is out'}
        except AttributeError:
          print('image is invalid')
          return {'error': 'iamge is invalid'}
        except Exception, ex:
          print(ex)
          return {'error':str(ex)}

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
