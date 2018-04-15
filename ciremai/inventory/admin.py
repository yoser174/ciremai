from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import Supplier,Location,Vendor,ProductLot,TemperatureCondition,Unit,Product,Storage,StockIn,StockInLot,Instrument,UsingProduct,UserExtension,ReturningProduct

# Define an inline admin descriptor
# which acts a bit like a singleton
class CRMUserProfileInline(admin.TabularInline):
    model = UserExtension
    can_delete = False
    extra = 1
    max_num = 1
    verbose_name_plural = _('User Profile Extensions')


# Define a new User admin
class NewUserAdmin(UserAdmin):
    inlines = (CRMUserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)


admin.site.register(Supplier)
admin.site.register(Location)
admin.site.register(Vendor)
admin.site.register(ProductLot)
admin.site.register(TemperatureCondition)
admin.site.register(Unit)
admin.site.register(Product)
admin.site.register(Storage)
admin.site.register(StockIn)
admin.site.register(StockInLot)
admin.site.register(Instrument)
admin.site.register(UsingProduct)
admin.site.register(ReturningProduct)
admin.site.register(UserExtension)