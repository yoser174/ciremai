# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import ReceivedSamples,Instruments,Results,OrderResults,TestParameters, \
TestRefRanges,InstrumentTests,InstrumentFlags

class InstTestInline(admin.TabularInline):
    model = InstrumentTests

class TestAdmin(admin.ModelAdmin):
    list_display = ('test','unit','decimal_place','method','special_information')
    search_fields = ['test','unit','decimal_place','method','special_information']
    list_filter = ('unit','decimal_place','method','special_information')
    
class TestRefAdmin(admin.ModelAdmin):
    list_display = ('test','gender','age_from','age_from_type','age_to','age_to_type','operator', \
                    'any_age','lower','upper','operator_value','alfa_value','special_info')
    list_filter = ('gender','operator','any_age','alfa_value')
    search_fields = ['test','gender','age_from','age_from_type','age_to','age_to_type','operator', \
                    'any_age','lower','upper','operator_value','alfa_value','special_info']

class InstTestAdmin(admin.ModelAdmin):
    list_display = ('instrument','test','test_code','result_type')
    

class InstAdmin(admin.ModelAdmin):
    list_display = ('code','name','active','driver','connection_type','serial_port','serial_baud_rate','serial_data_bit','serial_stop_bit',\
                    'serial_data_bit','tcp_conn_type','tcp_host','tcp_port')
    list_filter = ('code','name','active','driver','connection_type')
    search_fields = ['code','name','active','driver','connection_type','serial_port','serial_baud_rate','serial_data_bit','serial_stop_bit',\
                    'serial_data_bit','tcp_conn_type','tcp_host','tcp_port']
    inlines = [
        InstTestInline,
    ]
    

admin.site.register(ReceivedSamples)
admin.site.register(Instruments,InstAdmin)
admin.site.register(InstrumentTests,InstTestAdmin)
admin.site.register(InstrumentFlags)
admin.site.register(Results)
admin.site.register(OrderResults)
admin.site.register(TestParameters,TestAdmin)
admin.site.register(TestRefRanges,TestRefAdmin)
