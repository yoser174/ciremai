from django.contrib import admin
from .models import Tests,TestPrices,TestGroups,Priority,Insurance,Doctors,Genders,Patients,Orders,OrderTests,Parameters,Origins,Diagnosis

admin.site.register(Parameters)
admin.site.register(Tests)
admin.site.register(TestPrices)
admin.site.register(TestGroups)
admin.site.register(Priority)
admin.site.register(Origins)
admin.site.register(Insurance)
admin.site.register(Doctors)
admin.site.register(Genders)
admin.site.register(Patients)
admin.site.register(Orders)
admin.site.register(OrderTests)
admin.site.register(Diagnosis)


