# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import ReceivedSamples,Instruments,Results,OrderResults,TestParameters, \
TestRefRanges,InstrumentTests,InstrumentFlags

class TestAdmin(admin.ModelAdmin):
    list_display = ('test','unit','decimal','method','special_information')
    search_fields = ['test','unit','decimal','method','special_information']
    list_filter = ('unit','decimal','method','special_information')
    
class TestRefAdmin(admin.ModelAdmin):
    list_display = ('test','gender','age_from','age_from_type','age_to','age_to_type','operator', \
                    'any_age','lower','upper','operator_value','alfa_value','special_info')
    list_filter = ('gender','operator','any_age','alfa_value')
    search_fields = ['test','gender','age_from','age_from_type','age_to','age_to_type','operator', \
                    'any_age','lower','upper','operator_value','alfa_value','special_info']

admin.site.register(ReceivedSamples)
admin.site.register(Instruments)
admin.site.register(InstrumentTests)
admin.site.register(InstrumentFlags)
admin.site.register(Results)
admin.site.register(OrderResults)
admin.site.register(TestParameters,TestAdmin)
admin.site.register(TestRefRanges,TestRefAdmin)
