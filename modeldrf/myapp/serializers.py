from rest_framework import serializers
from .models import RandomPicker

class RandomPickerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RandomPicker
        fields = [
            'id',
            'start',
            'end',
            'result',
            'status',
            'url',
        ]
        read_only_fields = ['id', 'result', 'url']

# vim: et ai ts=4 sw=4 sts=4 ru nu
