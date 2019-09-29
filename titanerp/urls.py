"""titanerp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls import url, include
from django.conf.urls import url, include
from django.contrib import admin
# from django.urls import path, re_path, include
from django.views.static import serve
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from basedata import views
from titanerp.settings import MEDIA_ROOT
from web.views.base import LoginView

router = routers.DefaultRouter()
router.register(r'computers', views.ComputerAPIView, base_name='computer')
router.register(r'propetrys', views.PorpertyAPIView, base_name='propetry')
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='泰坦行政')

urlpatterns = [
    url(r'^docs/', include_docs_urls(title='泰坦科技')),
    url(r'^admin/', admin.site.urls,name='admin'),
    url(r'^api/basedata/', include('basedata.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # url(r'^login/', rbac_view.LoginView.as_view(),name='login'),
    # url(r'^reg/', rbac_view.reg,name='reg'),
    # url(r'^index/', rbac_view.index,name='index'),
    url(r'^web/',include('web.urls')),
    # url('',LoginView.as_view()),
    
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]
