# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from rest_framework import viewsets
from .models import RandomPicker
from .serializers import RandomPickerSerializer

logger = logging.getLogger('project_logging')

class RandomPickerViewSet(viewsets.ModelViewSet):

    queryset = RandomPicker.objects.all()
    serializer_class = RandomPickerSerializer
    http_method_names = ['head', 'options', 'post', 'get']

# vim: et ai ts=4 sw=4 sts=4 ru nu
