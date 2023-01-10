from django.urls import path
from . import views

urlpatterns = [
    path('product_list/<str:category>/<str:sub_category>/<str:sortby>/<str:min>/<str:max>/', views.product_list, name='product_list'),
    path('product_view/<int:id>', views.product_view, name='product_view'),
    path('get_size_info', views.get_size_info, name='get_size_info'),

]