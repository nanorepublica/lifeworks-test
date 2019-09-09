from .celery import celery


@celery.task()
def call_geoip_api(data):
    return 1 + 1
