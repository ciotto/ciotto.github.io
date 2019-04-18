from django.conf.urls import url
from ci8 import views
from ci8.views import pages

urlpatterns = [
    url(r'^%s$' % pages[0]['path'], views.index),
    url(r'^%s$' % pages[1]['path'], views.haier_t32x),
    url(r'^%s$' % pages[2]['path'], views.digipass_go_6),
    url(r'^sitemap.xml$', views.sitemap),
]
