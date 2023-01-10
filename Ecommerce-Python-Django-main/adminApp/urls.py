from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),


    path('admin_user_list', views.admin_user_list, name='admin_user_list'),
    path('block_unblock_user/<int:id>', views.block_unblock_user, name='block_unblock_user'),


    path('admin_product_list', views.admin_product_list, name='admin_product_list'),
    path('admin_add_product', views.admin_add_product, name='admin_add_product'),
    path('admin_delete_product/<int:id>', views.admin_delete_product, name='admin_delete_product'),
    path('admin_edit_product/<int:id>', views.admin_edit_product, name='admin_edit_product'),


    path('admin_category_management', views.admin_category_management, name='admin_category_management'),
    path('admin_add_category', views.admin_add_category, name='admin_add_category'),
    path('admin_add_sub_category', views.admin_add_sub_category, name='admin_add_sub_category'),
    path('admin_edit_category/<int:id>', views.admin_edit_category, name='admin_edit_category'),
    path('admin_edit_sub_category/<int:id>', views.admin_edit_sub_category, name='admin_edit_sub_category'),
    path('admin_delete_category/<int:id>', views.admin_delete_category, name='admin_delete_category'),
    path('admin_edit_sub_category/admin_delete_sub_category/<int:id>', views.admin_delete_sub_category, name='admin_delete_sub_category'),


    path('admin_order_list', views.admin_order_list, name='admin_order_list'),
    path('admin_order_details/<int:id>', views.admin_order_details, name='admin_order_details'),
    path('admin_order_change_status/<int:id>', views.admin_order_change_status, name='admin_order_change_status'),

    path('admin_coupons', views.admin_coupons, name='admin_coupons'),
    path('admin_add_coupon', views.admin_add_coupon, name='admin_add_coupon'),
    path('admin_delete_coupon/<int:id>', views.admin_delete_coupon, name='admin_delete_coupon'),
    path('admin_edit_coupon/<int:id>', views.admin_edit_coupon, name='admin_edit_coupon'),

    # path('admin_category_offers', views.admin_category_offers, name='admin_category_offers'),
    # path('admin_add_category_offer', views.admin_add_category_offer, name='admin_add_category_offer'),
    # path('admin_delete_category_offer/<int:id>', views.admin_delete_category_offer, name='admin_delete_category_offer'),
    # path('admin_active_category_offer/<int:id>', views.admin_active_category_offer, name='admin_active_category_offer'),

    # path('admin_product_offers', views.admin_product_offers, name='admin_product_offers'),
    # path('admin_add_product_offer', views.admin_add_product_offer, name='admin_add_product_offer'),
    # path('admin_delete_product_offer/<int:id>', views.admin_delete_product_offer, name='admin_delete_product_offer'),
    # path('admin_active_product_offer/<int:id>', views.admin_active_product_offer, name='admin_active_product_offer'),
 
    path('admin_sales_report', views.admin_sales_report, name='admin_sales_report'),
    path('admin_export_sales_reportCSV/<str:startDate>/<str:endDate>', views.admin_export_sales_reportCSV, name='admin_export_sales_reportCSV'),
    path('admin_export_sales_reportPDF/<str:startDate>/<str:endDate>', views.admin_export_sales_reportPDF, name='admin_export_sales_reportPDF'),
]