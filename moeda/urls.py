from django.urls import path

from .views import *

urlpatterns = [
    path('', MoedaView.as_view(), name='moeda'),
]
