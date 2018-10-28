from django.contrib import admin
from .models import Tests,TestPrices,TestGroups,Priority,Insurance,Doctors, \
Genders,Patients,Orders,OrderTests,Parameters,Origins,Diagnosis,SuperGroups, \
Specimens,LabelPrinters, Salutation, Article

class TestsInline(admin.TabularInline):
    model = Tests
    
class TestPriceInline(admin.TabularInline):
    model = TestPrices
    

class TestGroupAdmin(admin.ModelAdmin):
    search_fields = ['name','sort']
    list_display = ('name','sort')
    inlines = [
        TestsInline,
    ]
    
class LabelPrinterAdmin(admin.ModelAdmin):
    list_display = ('name','active','com_port')
    list_filter = ('name','active',)

class ParAdmin(admin.ModelAdmin):
    search_fields = ['name','char_value','num_value']
    list_display = ('name','char_value','num_value')
    
class NameSortdmin(admin.ModelAdmin):
    search_fields = ['name','sort']
    list_display = ('name','sort')
    
class NameExtAdmin(admin.ModelAdmin):
    search_fields = ['name','ext_code']
    list_display = ('name','ext_code')
    
class NameSuffixAdmin(admin.ModelAdmin):
    search_fields = ['name','suffix_code']
    list_display = ('name','suffix_code')
    
class TestAdmin(admin.ModelAdmin):
    search_fields = ['sort','name']
    list_display = ('sort','test_group','name','specimen','can_request','ext_code')
    list_filter = ('test_group__name','can_request',)
    inlines = [
        TestPriceInline,
    ]

    

admin.site.register(Parameters,ParAdmin)
admin.site.register(Tests,TestAdmin)
admin.site.register(TestPrices)
admin.site.register(TestGroups,TestGroupAdmin)
admin.site.register(Priority,NameExtAdmin)
admin.site.register(Origins,NameExtAdmin)
admin.site.register(Insurance,NameExtAdmin)
admin.site.register(Doctors,NameExtAdmin)
admin.site.register(Genders,NameExtAdmin)
admin.site.register(Salutation)
admin.site.register(Patients)
admin.site.register(Orders)
admin.site.register(Article)
admin.site.register(OrderTests)
admin.site.register(Diagnosis)
admin.site.register(SuperGroups)
admin.site.register(Specimens,NameSuffixAdmin)
admin.site.register(LabelPrinters,LabelPrinterAdmin)




