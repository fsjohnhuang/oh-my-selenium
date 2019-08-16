#!/usr/bin/env python
# -*- coding: utf-8 -*-
from oh_my_logging.builders import LoggerBuilderFactory
from oh_my_logging.decorators import logger

dict_conf = {
    'version': 1,
    'root': {
        'level': 'DEBUG',
        'handlers': ['simple'],
    },
    'handlers':{
        'simple': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'formatters': {
        'default': {
            'format': '%(message)s'
        }
    }
}

LoggerBuilderFactory(dict_conf)

@logger
def func(logger):
    logger.info('123')

func()
