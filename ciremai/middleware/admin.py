# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Specimens,Tubes,ReceivedSamples


admin.site.register(Specimens)
admin.site.register(Tubes)
admin.site.register(ReceivedSamples)