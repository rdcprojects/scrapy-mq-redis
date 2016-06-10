# -*- coding: utf-8 -*-
__author__ = 'rdchawda'

try:
    import pika
except ImportError:
    raise ImportError("Please install pika before running scrapy-rabbitmq.")
try:
    import redis
except ImportError:
    raise ImportError("Please install redis before running scrapy-rabbitmq")
import logging

RABBITMQ_CONNECTION_TYPE = 'blocking'
RABBITMQ_QUEUE_NAME = 'scrapy_queue'
RABBITMQ_CONNECTION_PARAMETERS = {'host': 'localhost'}
REDIS_URL = None
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

LOGGER = logging.getLogger(__name__)


def from_settings(settings):
    """
    :param: settings object
    :return: Channel object
    """

    connection_type = settings.get('RABBITMQ_CONNECTION_TYPE', RABBITMQ_CONNECTION_TYPE)
    connection_parameters = settings.get('RABBITMQ_CONNECTION_PARAMETERS', RABBITMQ_CONNECTION_PARAMETERS)

    connection = {
        'blocking': pika.BlockingConnection,
        'libev': pika.LibevConnection,
        'select': pika.SelectConnection,
        'tornado': pika.TornadoConnection,
        'twisted': pika.TwistedConnection
    }[connection_type](pika.ConnectionParameters(**connection_parameters))

    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)

    url = settings.get('REDIS_URL', REDIS_URL)
    host = settings.get('REDIS_HOST', REDIS_HOST)
    port = settings.get('REDIS_PORT', REDIS_PORT)

    # REDIS_URL takes precedence over host/port specification.
    if url:
        redis_server = redis.from_url(url)
    else:
        redis_server = redis.Redis(host=host, port=port)

    return channel, redis_server
