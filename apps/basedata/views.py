# Create your views here.
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from basedata.models import Computer, Property
from basedata.serializer import ComputerSerializer, PropertySerializer


class ComputerPageNumberPagination(PageNumberPagination):
    # 默认每页显示的个数
    page_size = 5
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 100


class ComputerAPIView(ModelViewSet):
    """
    list: 获取多个设备信息
    create: 创建一个设备
    read: 读取一个设备信息
    """
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer
    pagination_class = ComputerPageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name', 'memory')


class PorpertyAPIView(ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
