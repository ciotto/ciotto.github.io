from django.conf.urls import url
from ci8 import views

urlpatterns = [
    url(r'^index.html$', views.index),
    url(r'^haier-t32x.html$', views.haier_t32x),
]
