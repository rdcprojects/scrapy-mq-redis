import sys, os
import scrapy_mq_redis

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


packages = [
    'scrapy_mq_redis'
]

requires = [
    'pika',
    'redis',
    'scrapy_redis',
    'Scrapy>=0.14'
]

setup(
    name='scrapy-mq-redis',
    author='Rakesh Chawda',
    description='RabbitMQ / Redis Plug-in for Scrapy',
    version='0.1',
    author_email='rdchawda@gmail.com',
    license='GNU GPL3',
    url='https://github.com/rdcprojects/scrapy-mq-redis',
    install_requires=requires,
    packages=packages
)