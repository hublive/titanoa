# encoding: utf-8
import django_filters
from basedata.models import Computer


class ComputerFilter(django_filters.filterset):
    class Meta:
        model = Computer
        fields = "__all__"
