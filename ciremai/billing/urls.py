from __future__ import unicode_literals

from django.conf.urls import  url,include
from . import views

urlpatterns = [
    
    url("^$", views.home, name="home_billing"),
    url(r'^dashboard/$', views.show_dashboard, name='dashboard_billing'),
    url(r'^login/$', views.login_user, name='login_billing'),
    url(r'^logout/$', views.login_user, name='logout_biling'),
    url(r'^avatarchange/$', views.AvatarChange, name='avatar_change_billing'),
    url(r'^avataradd/$', views.AvatarAdd, name='avatar_add_billing'),
    
    url(r'^profileupdate/(?P<pk>\d+)/$', views.UpdateUserProfile, name='profile_update_billing'),
    
    # #############
    # Test Groups urls
    # #############
    url(r'^testgroups/$', views.ListTestGroups.as_view(), name='testgroups_list'),
    url(r'^testgroups/detail/(?P<pk>\d+)/$', views.ListTestGroups.as_view(), name='testgroups_detail'),
    url(r'^testgroups/create/$', views.CreateTestGroup.as_view(), name='testgroups_create'),
    url(r'^testgroups/edit/(?P<pk>\d+)/$', views.EditTestGroup.as_view(), name='testgroups_edit'),
    url(r'^testgroups/delete/(?P<pk>\d+)/$', views.DeleteTestGroup.as_view(), name='testgroups_delete'),
    
    # #############
    # Tests urls
    # #############
    url(r'^tests/$', views.ListTests.as_view(), name='tests_list'),
    url(r'^tests/detail/(?P<pk>\d+)/$', views.ListTests.as_view(), name='tests_detail'),
    url(r'^tests/create/$', views.CreateTests.as_view(), name='tests_create'),
    url(r'^tests/edit/(?P<pk>\d+)/$', views.EditTests.as_view(), name='tests_edit'),
    url(r'^tests/delete/(?P<pk>\d+)/$', views.DeleteTests.as_view(), name='tests_delete'),
    
    # #############
    # Order urls
    # #############
    url(r'^orders/$', views.ListOrders.as_view(), name='orders_list'),
    url(r'^orders/edit/(?P<pk>\d+)/$', views.EditOrder.as_view(), name='order_edit'),
    url(r'^orders/patient/$', views.order_patient, name='order_patient'),
    url(r'^orders/delete/(?P<pk>\d+)/$', views.DeleteOrder.as_view(), name='order_delete'),
    url(r'^orders/add/patient/$', views.order_add_patient, name='order_add_patient'),
    url(r'^orders/patient/create/(?P<patient_pk>\d+)/$', views.create_order_from_patient, name='create_order_from_patient'),
    url(r'^orders/detail/(?P<pk>\d+)/$', views.order_entry, name='order_detail'),
    url(r'^orders/detail/(?P<order_pk>\d+)/payment', views.order_payment, name='order_payment'),
    url(r'^orders/detail/(?P<order_pk>\d+)/delete', views.order_delete_test, name='order_delete_test'),
    url(r'^orders/detail/(?P<order_pk>\d+)/print/receipt$', views.order_print_receipt, name='order_print_receipt'),
    url(r'^orders/detail/(?P<order_pk>\d+)/print/bill$', views.order_print_bill, name='order_print_bill'),
    url(r'^orders/detail/(?P<order_pk>\d+)/print/worklist$', views.order_print_worklist, name='order_print_worklist'),
    url(r'^orders/detail/(?P<order_pk>\d+)/label', views.order_print_barcode, name='order_barcode'), 
    url(r'^orders/detail/(?P<order_pk>\d+)/send/lis$', views.order_send_lis, name='order_send_lis'),
    url(r'^orders/detail/(?P<order_pk>\d+)/replace_test_from$', views.replace_test_from, name='replace_test_from'),
    
    # #############
    # Patient urls
    # #############
    url(r'^patients/$', views.ListPatients.as_view(), name='patients_list'),
    url(r'^patients/detail/(?P<pk>\d+)/$', views.ViewPatients.as_view(), name='patient_detail'),
    url(r'^patients/create/$', views.CreatePatient.as_view(), name='patient_create'),
    url(r'^patients/edit/(?P<pk>\d+)/$', views.EditPatient.as_view(), name='patient_edit'),
    url(r'^patients/delete/(?P<pk>\d+)/$', views.DeletePatient.as_view(), name='patient_delete'),
    
    # #############
    # Doctors urls
    # #############
    url(r'^doctors/$', views.ListDoctors.as_view(), name='doctors_list'),
    url(r'^doctors/detail/(?P<pk>\d+)/$', views.ViewDoctors.as_view(), name='doctor_detail'),
    url(r'^doctors/create/$', views.CreateDoctor.as_view(), name='doctor_create'),
    url(r'^doctors/edit/(?P<pk>\d+)/$', views.EditDoctor.as_view(), name='doctor_edit'),
    url(r'^doctors/delete/(?P<pk>\d+)/$', views.DeleteDoctor.as_view(), name='doctor_delete'),
    
     # #############
    # Report urls
    # #############
    url(r'^reports/jm/$', views.report_jm, name='jm_list'),
    url(r'^reports/origin/$', views.report_origin, name='origin_list'),
    url(r'^reports/insurance/$', views.report_insurance, name='insurance_list'),
    url(r'^reports/tests/$', views.report_tests, name='tests_list'),
    
    url(r'^avatar/', include('avatar.urls')),
    ]