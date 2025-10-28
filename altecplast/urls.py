from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('simulateur/', views.simulateur_form_view, name='simulateur'),
    path('weighing/', views.weighing_form_view, name='weighing'),
    path('dashboard-login/', views.dashboard_login_view, name='dashboard_login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/data/', views.dashboard_data_view, name='dashboard_data'),
    path('production/', views.production_view, name='production'),
    path('admin/', views.admin_page, name='admin'),
    path('referenced-entry/', views.referenced_entry_view, name='referenced_entry'),
    path('non-referenced-entry/', views.non_referenced_entry_view, name='non_referenced_entry'),
    path('finished-product-output/', views.finished_product_output_view, name='finished_product_output'),
    path('waste-output/', views.waste_output_view, name='waste_output'),
    path('finished-product-return/', views.finished_product_return_view, name='finished_product_return'),
    path('merchandise-return/', views.merchandise_return_view, name='merchandise_return'),
    path('outsourced-product-output/', views.outsourced_product_output_view, name='outsourced_product_output'),
    path('outsourced-product-return/', views.outsourced_product_return_view, name='outsourced_product_return'),
    path('api/supplier-defaults/', views.get_supplier_defaults, name='get_supplier_defaults'),
    path('api/client-defaults/', views.get_client_defaults, name='get_client_defaults'),
    path('api/waste-client-defaults/', views.get_waste_client_defaults, name='get_waste_client_defaults'),
]