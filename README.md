## A RabbitMQ /Redis plugin for Scrapy Framework.

Scrapy-mq-redis is a tool that lets you feed and queue URLs from RabbitMQ via Scrapy spiders, using the [Scrapy framework](http://doc.scrapy.org/en/latest/index.html).

It uses Redis for DupeFilter

Made using a combination of [scrapy-rabbitmq](https://github.com/roycehaynes/scrapy-rabbitmq/) and [scrapy-redis](https://github.com/darkrho/scrapy-redis).

## Installation

Clone the repo and inside the scrapy-mq-redis directory, type

```
python setup.py install
```

## Preparation

Below queues will have to created in RabbitMQ before starting the crawl:

* ${spider_name}:start_urls
* ${spider_name}:requests
* ${spider_name}:items

Note: Will be adding automatic queue creation soon.

## Usage

### Step 1: In your scrapy settings, add the following config values:

```
# Enables scheduling storing requests queue in rabbitmq.

SCHEDULER = "scrapy_rabbitmq.scheduler.Scheduler"

# Don't cleanup rabbitmq queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = True

# Schedule requests using a priority queue. (default)
SCHEDULER_QUEUE_CLASS = 'scrapy_rabbitmq.queue.SpiderQueue'

# Provide host and port to RabbitMQ daemon
RABBITMQ_CONNECTION_PARAMETERS = {'host': 'localhost', 'port': 6666}

# Store scraped item in rabbitmq for post-processing.
ITEM_PIPELINES = {
    'scrapy_rabbitmq.pipelines.RabbitMQPipeline': 1
}

REDIS_HOST = '192.168.1.200'
REDIS_PORT = 6379

```

### Step 2: Add RabbitMQMixin to Spider.

#### Example: multidomain_spider.py

```
from scrapy.contrib.spiders import CrawlSpider
from scrapy_mq_redis.spiders import RabbitMQMixin

class MultiDomainSpider(RabbitMQMixin, CrawlSpider):
    name = 'multidomain'

    def parse(self, response):
        # parse all the things
        pass

```

### Step 3: Run spider using [scrapy client](http://doc.scrapy.org/en/1.0/topics/shell.html)

```
scrapy runspider multidomain_spider.py
```

### Step 4: Push URLs to RabbitMQ

#### Example: push_web_page_to_queue.py

```
#!/usr/bin/env python
import pika
import settings

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()

channel.basic_publish(exchange='',
                      routing_key='spider:start_urls',
                      body='</html>raw html contents<a href="http://twitter.com/roycehaynes">extract url</a></html>')

connection.close()

```

## Contributing and Forking

See [Contributing Guidlines](CONTRIBUTING.MD)

## Releases

See the [changelog](CHANGELOG.md) for release details.

| Version | Release Date |
| :-----: | :----------: |
| 0.1.0 | 2016-6-2 |



## Copyright & License

Copyright (c) 2016 Rakesh Chawda - Released under the GNU GPL3 License.
