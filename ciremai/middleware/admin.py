# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import ReceivedSamples,Instruments,Results,OrderResults,TestParameters,TestRefRanges,InstrumentTests,InstrumentFlags


admin.site.register(ReceivedSamples)
admin.site.register(Instruments)
admin.site.register(InstrumentTests)
admin.site.register(InstrumentFlags)
admin.site.register(Results)
admin.site.register(OrderResults)
admin.site.register(TestParameters)
admin.site.register(TestRefRanges)