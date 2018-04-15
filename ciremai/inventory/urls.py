from __future__ import unicode_literals

from django.conf.urls import  url,include
from .views import direct_to_template
from . import views


urlpatterns = [
    
    url("^$", direct_to_template, {"template": "index.html"}, name="home"),
    url(r'^dashboard/$', views.show_dashboard, name='dashboard'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.login_user, name='logout'),
    url(r'^avatarchange/$', views.AvatarChange, name='avatar_change'),
    url(r'^avataradd/$', views.AvatarAdd, name='avatar_add'),
    #url(r'^avatar/', include('avatar.urls')),
    url(r'^profileupdate/(?P<pk>\d+)/$', views.UpdateUserProfile.as_view(), name='profile_update'),
    
    # #############
    # Supplier urls
    # #############
    url(r'^suppliers/$', views.ListSuppliers.as_view(), name='supplier_list'),
    url(r'^suppliers/detail/(?P<pk>\d+)/$', views.ViewSupplier.as_view(), name='supplier_detail'),
    url(r'^suppliers/create/$', views.CreateSupplier.as_view(), name='supplier_create'),
    url(r'^suppliers/edit/(?P<pk>\d+)/$', views.EditSupplier.as_view(), name='supplier_edit'),
    url(r'^suppliers/delete/(?P<pk>\d+)/$', views.DeleteSupplier.as_view(), name='supplier_delete'),
    
    # #############
    # Vendor urls
    # #############
    url(r'^vendors/$', views.ListVendors.as_view(), name='vendor_list'),
    url(r'^vendors/detail/(?P<pk>\d+)/$', views.ViewVendor.as_view(), name='vendor_detail'),
    url(r'^vendors/create/$', views.CreateVendor.as_view(), name='vendor_create'),
    url(r'^vendors/edit/(?P<pk>\d+)/$', views.EditVendor.as_view(), name='vendor_edit'),
    url(r'^vendors/delete/(?P<pk>\d+)/$', views.DeleteVendor.as_view(), name='vendor_delete'),
    
     # ############
     # Product urls
     # ############
     url(r'^products/$', views.ListProducts.as_view(), name='product_list'),
     url(r'^products/create/$', views.CreateProduct.as_view(), name='product_create'),
     url(r'^products/detail/(?P<pk>\d+)/$', views.ViewProduct.as_view(), name='product_detail'),
     url(r'^products/edit/(?P<pk>\d+)/$', views.EditProduct.as_view(), name='product_edit'),
     url(r'^products/delete/(?P<pk>\d+)/$', views.DeleteProduct.as_view(), name='product_delete'),
     
    # ############
     # Stock in urls
     # ############
     url(r'^stockin/$', views.ListStockin.as_view(), name='stockin_list'),
     url(r'^stockin/create/$', views.CreateStockin.as_view(), name='stockin_create'),
     url(r'^stockin/detail/(?P<pk>\d+)/$', views.ViewStockin.as_view(), name='stockin_detail'),
     url(r'^stockin/edit/(?P<pk>\d+)/$', views.EditStockin.as_view(), name='stockin_edit'),
     url(r'^stockin/delete/(?P<pk>\d+)/$', views.DeleteStockin.as_view(), name='stockin_delete'),
     url(r'^stockin/lot/(?P<pk>\d+)/$', views.EditStockinLot.as_view(), name='stockin_lot'),
     
     # ############
     # Using products in urls
     # ############
     url(r'^usingproduct/$', views.ListUsingProduct.as_view(), name='usingproduct_list'),
     url(r'^usingproduct/storage/$', views.using_product_storage, name='select_storage'),
     url(r'^usingproduct/stockin/(?P<storage_pk>\d+)$', views.using_product_select_stockin, name='select_stockin'),
     url(r'^usingproduct/stockin/create/(?P<stockin_pk>\d+)$', views.create_usingproduct_from_stockin, name='stockin_create_usingproduct'),
     url(r'^usingproduct/edit/(?P<pk>\d+)/$', views.EditUsingProduct.as_view(), name='usingproduct_edit'),
     url(r'^usingproduct/delete/(?P<pk>\d+)/$', views.DeleteUsingProduct.as_view(), name='usingproduct_delete'),
     
     # ############
     # Returning products in urls
     # ############
     url(r'^returningproduct/$', views.ListReturningProduct.as_view(), name='returningproduct_list'),
     url(r'^returningproduct/instrument/$', views.returning_product_instrument, name='select_instrument'),
     url(r'^returningproduct/usingproduct/(?P<instrument_pk>\d+)$', views.returning_product_select_using, name='select_usingproduct'),
     url(r'^returningproduct/usingproduct/create/(?P<usingproduct_pk>\d+)$', views.create_returnproduct_from_use, name='using_create_return'),
     url(r'^returningproduct/edit/(?P<pk>\d+)/$', views.EditReturningProduct.as_view(), name='returningproduct_edit'),
     url(r'^returningproduct/delete/(?P<pk>\d+)/$', views.DeleteReturningProduct.as_view(), name='returningproduct_delete'),
     
     # ############
     # Report in urls
     # ############
     url(r'^stock/$', views.view_available_stock, name='productstock_list'),
     url(r'^stock/csv/$', views.view_available_stock_csv,name='productstock_csv')
    ]