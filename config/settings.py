import os


CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5

SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
DATABASE = {
    'HOST': 'db',
    'PORT': 8086,
    'USER': 'root',
    'PASS': 'root',
    'NAME': 'event_store'
}
