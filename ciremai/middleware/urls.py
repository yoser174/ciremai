from __future__ import unicode_literals

from django.conf.urls import  url
from billing.views import direct_to_template
from . import views

urlpatterns = [
    
    url("^$", direct_to_template, {"template": "index_middleware.html"}, name="home"),
    #url(r'^dashboard/$', views.show_dashboard, name='dashboard_billing'),
    #url(r'^login/$', views.login_user, name='login'),
    #url(r'^logout/$', views.login_user, name='logout'),
    #url(r'^avatarchange/$', views.AvatarChange, name='avatar_change'),
    #url(r'^avataradd/$', views.AvatarAdd, name='avatar_add'),
    #url(r'^avatar/', include('avatar.urls')),
    #url(r'^profileupdate/(?P<pk>\d+)/$', views.UpdateUserProfile.as_view(), name='profile_update'),
    
    #################
    # Receive sample
    #################
    url(r'^rcvsample/$', views.ListReceivedSample.as_view(), name='receivedsample_list'),
    
    
    # #############
    # Test Groups urls
    # #############
    #url(r'^testgroups/$', views.ListTestGroups.as_view(), name='testgroups_list'),
    #url(r'^testgroups/detail/(?P<pk>\d+)/$', views.ListTestGroups.as_view(), name='testgroups_detail'),
    #url(r'^testgroups/create/$', views.CreateTestGroup.as_view(), name='testgroups_create'),
    #url(r'^testgroups/edit/(?P<pk>\d+)/$', views.EditTestGroup.as_view(), name='testgroups_edit'),
    #url(r'^testgroups/delete/(?P<pk>\d+)/$', views.DeleteTestGroup.as_view(), name='testgroups_delete'),
    
   
    ]