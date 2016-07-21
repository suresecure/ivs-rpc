from kombu import Queue, Exchange
# SECRET_KEY = 'not_a_secret'
# CELERY_BROKER_URL='redis://localhost:6379/0'
# CELERY_RESULT_BACKEND='redis://localhost:6379/0'
CELERY_BROKER_URL='amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND='amqp://guest:guest@localhost:5672//'
CELERYD_CONCURRENCY = 1
CELERYD_PREFETCH_MULTIPLIER = 0

CELERY_QUEUES = (
    Queue(
        'important',
        exchange=Exchange('important'),
        routing_key="important",
        queue_arguments={'x-max-length': 1}
    ),
)
