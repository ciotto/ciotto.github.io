from django.conf.urls import url
from ci8 import views

urlpatterns = [
    url(r'^%s$' % views.home_page['path'], views.index),
    url(r'^%s$' % views.about_me_page['path'], views.about_me),
    url(r'^%s$' % views.haier_t32x_page['path'], views.haier_t32x),
    url(r'^%s$' % views.digipass_go_6_page['path'], views.digipass_go_6),
    url(r'^sitemap.xml$', views.sitemap),
]
