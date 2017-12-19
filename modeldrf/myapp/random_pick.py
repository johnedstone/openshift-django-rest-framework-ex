# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from random import randint

try:
    # logging in the context of django
    from django.conf import settings
    logger = logging.getLogger('project_logging')
except ImportError:
    # logging when running outside the context of django
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s:%(module)s:%(lineno)d:%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def get_rand_int(start, end):
    result = {
        'success': 'Fail',
        'random_result': None,
    }

    rand_int = randint(start, end)
    result['random_result'] = rand_int

    logger.info('Random result: {}'.format(rand_int))

    logger.info('Is the result divisible by 2 (0=yes, 1=no): {}'.format(rand_int % 2))
    if rand_int % 2 == 0:
        result['success'] = 'Pass'

    return result

if __name__ == '__main__':
    result = get_rand_int(1, 100)
    logger.info('result: {}'.format(result))

# vim: et ai ts=4 sw=4 sts=4 ru nu
