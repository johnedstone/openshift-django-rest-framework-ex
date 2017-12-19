# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.conf import settings
from rest_framework.response import Response
from rest_framework import viewsets, status

from . import RandomPicker
from . import serializers
from . import random_pick

logger = logging.getLogger('project_logging')

class RandomPickerViewSet(viewsets.ViewSet):
    """Based on 

    https://github.com/linovia/drf-demo/blob/master/drf_demo/model_less/views.py
    """

    http_method_names = ['head', 'options', 'post', 'get']

    def list(self, request):
        '''Sample of returning a list of objects
        
        Which could be built dynamically from another job, query, etc.
        '''

        sample_picks = {
            'a': RandomPicker(start=1,
                end=10,
                status='Pass',
                result=8),
            'b': RandomPicker(start=10,
                end=100,
                status='Fail',
                result=89),
            'c': RandomPicker(start=100,
                end=1000,
                status='Pass',
                result=898),

        }

        serializer = serializers.RandomPickerSerializer(
                    instance=sample_picks.values(), many=True)

        return Response(serializer.data)
              

    def create(self, request):
        ''' Sample of posting some data.
        
        The result returned could be from another job, function call,
        which in this case is the random-pick.get_rand_int function.
        '''

        logger.info(request.data)
        serializer = serializers.RandomPickerSerializer(data=request.data)
        if serializer.is_valid():
            random_picker = serializer.save()
            logger.info('serialized random_picker: {}'.format(random_picker))

            result = random_pick.get_rand_int(random_picker.start, random_picker.end)
            logger.info('result: {}'.format(result))

            # Update serializer with results
            serializer.instance.result = result['random_result']
            serializer.instance.status = result['success']


            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# vim: et ai ts=4 sw=4 sts=4 ru nu
