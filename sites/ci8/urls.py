from django.conf.urls import url
from ci8 import views
from ci8.views import pages

urlpatterns = [
    url(r'^%s$' % pages[0][1], views.index),
    url(r'^%s$' % pages[1][1], views.haier_t32x),
    url(r'^%s$' % pages[2][1], views.digipass_go_6),
]
