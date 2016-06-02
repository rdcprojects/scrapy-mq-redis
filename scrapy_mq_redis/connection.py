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
    """ Factory method that returns an instance of channel

        :param str connection_type: This field can be `blocking`
            `asyncore`, `libev`, `select`, `tornado`, or `twisted`

        See pika documentation for more details:
            TODO: put pika url regarding connection type

        Parameters is a dictionary that can
        include the following values:

            :param str host: Hostname or IP Address to connect to
            :param int port: TCP port to connect to
            :param str virtual_host: RabbitMQ virtual host to use
            :param pika.credentials.Credentials credentials: auth credentials
            :param int channel_max: Maximum number of channels to allow
            :param int frame_max: The maximum byte size for an AMQP frame
            :param int heartbeat_interval: How often to send heartbeats
            :param bool ssl: Enable SSL
            :param dict ssl_options: Arguments passed to ssl.wrap_socket as
            :param int connection_attempts: Maximum number of retry attempts
            :param int|float retry_delay: Time to wait in seconds, before the next
            :param int|float socket_timeout: Use for high latency networks
            :param str locale: Set the locale value
            :param bool backpressure_detection: Toggle backpressure detection

        :return: Channel object
    """

    connection_type = settings.get('RABBITMQ_CONNECTION_TYPE', RABBITMQ_CONNECTION_TYPE)
    queue_name = settings.get('RABBITMQ_QUEUE_NAME', RABBITMQ_QUEUE_NAME)
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
    LOGGER.debug("New Channel: %s" % channel)
    # channel.queue_declare(queue=queue_name, durable=True)

    url = settings.get('REDIS_URL', REDIS_URL)
    host = settings.get('REDIS_HOST', REDIS_HOST)
    port = settings.get('REDIS_PORT', REDIS_PORT)

    # REDIS_URL takes precedence over host/port specification.
    if url:
        redis_server = redis.from_url(url)
    else:
        redis_server = redis.Redis(host=host, port=port)

    return channel, redis_server
