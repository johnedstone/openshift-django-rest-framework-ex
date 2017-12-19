# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.db import models
from . import random_pick

logger = logging.getLogger('project_logging')

class RandomPicker(models.Model):

    start = models.IntegerField()
    end = models.IntegerField()
    result = models.IntegerField(default=None)
    status = models.CharField(max_length=10, default='')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return 'RandomPick id: {}, result: {}, status: {}'.format(self.id, self.result, self.status)

    def save(self, *args, **kwargs):
        result = random_pick.get_rand_int(self.start, self.end)
        self.result = result['random_result']
        self.status = result['success']

        super(RandomPicker, self).save(*args, **kwargs)

# vim: et ai ts=4 sw=4 sts=4 ru nu
