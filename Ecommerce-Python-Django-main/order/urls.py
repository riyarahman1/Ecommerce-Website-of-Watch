from django.urls import path
from . import views

urlpatterns = [
    path('order_confirmation', views.order_confirmation, name='order_confirmation')
]