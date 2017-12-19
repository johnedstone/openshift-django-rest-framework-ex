from rest_framework import serializers
from . import RandomPicker

class RandomPickerSerializer(serializers.Serializer):

    start = serializers.IntegerField()
    end = serializers.IntegerField()
    result = serializers.IntegerField(default=None)
    status = serializers.CharField(max_length=10, default='')

    def create(self, validated_data):
        return RandomPicker(**validated_data)

# vim: et ai ts=4 sw=4 sts=4 ru nu
