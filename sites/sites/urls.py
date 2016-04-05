"""sites URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from staticsites.utilities import get_default_index, get_deploy_root
from ci8.urls import urlpatterns as ci8

urlpatterns = [
    url(r'^ci8/', include(ci8)),
]

# Serve default deploy folder as site root
if settings.DEBUG:
    from django.views.static import serve
    urlpatterns = [
        url(
            r'^(?:%s)?$' % get_default_index(deploy_type='dev'),
            serve,
            {
                'document_root': get_deploy_root(deploy_type='dev'), 'path': get_default_index(deploy_type='dev')
            }
        ),
        url(
            r'^(?P<path>.*)$',
            serve,
            {
                'document_root': get_deploy_root(deploy_type='dev')
            }
        ),
    ]
