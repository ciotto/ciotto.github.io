from django.conf.urls import url
from ci8 import views

urlpatterns = [
    url(r'^index.html$', views.index),
]
