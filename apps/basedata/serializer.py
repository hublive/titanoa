# encoding: utf-8

from rest_framework import serializers
from basedata.models import Computer, Property


class ComputerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Computer
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        depth = 2



