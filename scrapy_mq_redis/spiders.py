__author__ = 'rdchawda'

from . import connection
from scrapy.spiders import Spider
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
import logging

LOGGER = logging.getLogger(__name__)


class RabbitMQMixin(object):
    """ A RabbitMQ Mixin used to read URLs from a RabbitMQ queue.
    """

    rabbitmq_key = None

    def setup_rabbitmq(self):
        """ Setup RabbitMQ connection.

            Call this method after spider has set its crawler object.
        :return: None
        """

        if not self.rabbitmq_key:
            self.rabbitmq_key = '{}:start_urls'.format(self.name)

        self.server, self.redis_server = connection.from_settings(self.crawler.settings)

        self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

    def start_requests(self):
        method_frame, header_frame, url = self.server.basic_get(queue=self.rabbitmq_key)
        while url:
            yield self.make_requests_from_url(url)
            self.server.basic_ack(method_frame.delivery_tag)
            method_frame, header_frame, url = self.server.basic_get(queue=self.rabbitmq_key)

    def next_requests(self):
        self.start_requests()

    def spider_idle(self):
        """ Waits for request to be scheduled.

        :return: None
        """
        self.crawler.engine.slot.scheduler.next_request()
        raise DontCloseSpider

    def _set_crawler(self, crawler):
        super(RabbitMQMixin, self)._set_crawler(crawler)
        self.setup_rabbitmq()


class RabbitMQSpider(RabbitMQMixin, Spider):
    """ Spider that reads urls from RabbitMQ queue when idle.
    """
