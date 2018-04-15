# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Specimens,Tubes,ReceivedSamples,Instruments,Results,OrderResults


admin.site.register(Specimens)
admin.site.register(Tubes)
admin.site.register(ReceivedSamples)
admin.site.register(Instruments)
admin.site.register(Results)
admin.site.register(OrderResults)