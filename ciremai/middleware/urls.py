from __future__ import unicode_literals

from django.conf.urls import  url
from billing.views import direct_to_template
from . import views

urlpatterns = [
    
    url("^$", direct_to_template, {"template": "index_middleware.html"}, name="home_middleware"),
    url(r'^dashboard/$', views.show_dashboard, name='dashboard_middleware'),
    url(r'^login/$', views.login_user, name='login_middleware'),
    url(r'^logout/$', views.login_user, name='logout_middleware'),
    url(r'^avatarchange/$', views.AvatarChange, name='avatar_change_middleware'),
    url(r'^avataradd/$', views.AvatarAdd, name='avatar_add_middleware'),
    #url(r'^avatar/', include('avatar.urls')),
    url(r'^profileupdate/(?P<pk>\d+)/$', views.UpdateUserProfileMW.as_view(), name='profile_update_middleware'),
    
    #################
    # Receive sample
    #################
    url(r'^rcvsample/$', views.ListReceivedSample.as_view(), name='receivedsample_list'),
    
    #################
    # Order Results
    #################
    url(r'^orders/$', views.show_all_orders, name='orders'),
    url(r'^orders/results/(?P<pk>\d+)/$', views.order_results, name='order_results'),
    #url(r'^orders/results/(?P<pk>\d+)/validate/$', views.order_results_validate, name='order_results_validate'),
    url(r'^orders/results/(?P<pk>\d+)/techval/$', views.order_results_techval, name='order_results_techval'),
    url(r'^orders/results/(?P<pk>\d+)/medval/$', views.order_results_medval, name='order_results_medval'),
    url(r'^orders/results/(?P<pk>\d+)/print/$', views.order_results_print, name='order_results_print'),
    url(r'^orders/results/(?P<pk>\d+)/repeat/$', views.order_results_repeat, name='order_results_repeat'),
    url(r'^orders/results/(?P<pk>\d+)/history/$', views.order_results_history, name='order_results_history'),
    url(r'^orders/resultreport/(?P<pk>\d+)/$', views.order_result_report, name='order_results_report'),
    
    
    
    # #############
    # Test Groups urls
    # #############
    #url(r'^testgroups/$', views.ListTestGroups.as_view(), name='testgroups_list'),
    #url(r'^testgroups/detail/(?P<pk>\d+)/$', views.ListTestGroups.as_view(), name='testgroups_detail'),
    #url(r'^testgroups/create/$', views.CreateTestGroup.as_view(), name='testgroups_create'),
    #url(r'^testgroups/edit/(?P<pk>\d+)/$', views.EditTestGroup.as_view(), name='testgroups_edit'),
    #url(r'^testgroups/delete/(?P<pk>\d+)/$', views.DeleteTestGroup.as_view(), name='testgroups_delete'),
    
   
    ]