from __future__ import unicode_literals

from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.urlresolvers import reverse
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from annoying.fields import AutoOneToOneField
from simple_history.models import HistoricalRecords
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField




class Location(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
        
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class UserExtension(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='extension', verbose_name=_('Benutzer'))
    location = models.OneToOneField(Location, related_name='extension', verbose_name=_('Location'))
    image = models.ImageField(
        upload_to='avatars/', default='avatars/avatar.jpg', verbose_name=_('Bild'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('User Extension')
        verbose_name_plural = _('User Extensions')

    def __unicode__(self):
        return self.user.__unicode__()
    

class Vendor(models.Model):
    name = models.CharField(max_length=64)
    rep = models.CharField(max_length=45, blank=True, null=True)
    rep_phone = models.CharField(max_length=16, blank=True, null=True)
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('vendor_detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Vendor")
        verbose_name_plural = _("Vendors")
        permissions = (
            ('view_vendor', 'Can view vendors'),
        )


class Supplier(models.Model):
    name = models.CharField(max_length=64)
    rep = models.CharField(max_length=45, blank=True, null=True,help_text="contact person name")
    rep_phone = models.CharField(max_length=16, blank=True, null=True,help_text="contact telp")
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('supplier_detail', args=[str(self.id)])

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")
        permissions = (
            ('view_supplier', 'Can view suppliers'),
        )
    
class TemperatureCondition(models.Model):
    name =  models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
            
class Unit(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        
        
class Product(models.Model):
    number = models.CharField(max_length=30,help_text="Product number (eq: SKU or GTIN)")
    name = models.CharField(max_length=200,help_text="Product name")
    active = models.BooleanField()
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    base_unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    lot_controlled = models.BooleanField()
    temperature_condition = models.ForeignKey(TemperatureCondition, on_delete=models.PROTECT)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    lead_time = models.IntegerField(verbose_name=_("Lead time"),help_text=_("Lead time in day(s)"))
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])
    
    def __str__(self):
        return "%s %s %s" % (self.number,self.vendor,self.name)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        permissions = (
            ('view_product', 'Can view products'),
        )
        ordering = ['name']
        
class ProductLot(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    number =  models.IntegerField(verbose_name=_("Lot number"))
    expired = models.DateField(verbose_name=_("Expired at"))
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])
    
    def __str__(self):
        return "%s %s %s" % (self.product,self.number,self.expired)

    class Meta:
        verbose_name = _("Product Lot")
        verbose_name_plural = _("Product Lots")
        permissions = (
            ('view_productlot', 'Can view product lots'),
        )
        ordering = ['product']
    


        
class Storage(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
        
    def __str__(self):
        return "[%s] %s" % (self.location,self.name)

    class Meta:
        ordering = ['name']

class StockIn(models.Model):
    date_in = models.DateField(verbose_name=_("Date in"),auto_now_add=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    storage = models.ForeignKey(Storage, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = CurrentUserField()
    history = HistoricalRecords()
    
    @property
    def stockin_lot(self):
        try:
            return self._stockin_lot
        except StockInLot.DoesNotExist:
            return StockInLot.objects.create(
                stok_in=self,
            )
            
    def create_usingproduct(self, request):
        usingproduct = UsingProduct()
        usingproduct.stock_in = self
        usingproduct.save()
        return usingproduct
            
    def get_stockin_lot_url(self):
        return self._stockin_lot.get_absolute_url()
        
    
    def get_absolute_url(self):
        return reverse('receivelogistic_detail', args=[str(self.id)])
    
    def get_row_icon(self):
        if self.product.lot_controlled and not self.product_lot:
            return """%s <i class="fa fa-exclamation-circle" aria-hidden="true"></i>""" % self.product
        else:
            return "%s" % self.product
        
    def get_lot_url(self):
        return self.product.get_absolute_url()
        
        
    def has_lot(self):
        return bool(self.product.lot_controlled)
    
     
    def __str__(self):
        return "%s %s %s %s %s %s" %(self.supplier.name,self.product.number,self.product.vendor, self.product.name, self.quantity,self.product.base_unit)

    class Meta:
        ordering = ['-lastmodification']
        
class StockInLot(models.Model):
    stock_in = AutoOneToOneField(StockIn, related_name='_stockin_lot')
    number =  models.CharField(max_length=30,verbose_name=_("Lot number"),null=True)
    expired = models.DateField(verbose_name=_("Expired at"),null=True)
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    

    
    def get_absolute_url(self):
        return reverse('stockin_lot', args=[str(self.id)])
     
    def __str__(self):
        return "%s %s" %(self.number,self.expired)

    class Meta:
        ordering = ['-lastmodification']

    

class Instrument(models.Model):
    vendor =  models.ForeignKey(Vendor, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class UsingProduct(models.Model):
    date_use = models.DateField(verbose_name=_("Date used"),auto_now_add=True)
    stock_in = models.ForeignKey(StockIn, on_delete=models.PROTECT)
    unit_used = models.IntegerField(default=1)
    used_at = models.ForeignKey(Instrument, on_delete=models.PROTECT, null=True)
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby =  CurrentUserField()
    history = HistoricalRecords()
    
    
    def create_returningproduct(self, request):
        returningproduct = ReturningProduct()
        returningproduct.using_product = self
        returningproduct.save()
        return returningproduct
    
    def get_absolute_url(self):
        return reverse('usingproduct_detail', args=[str(self.id)])
    
    def __str__(self):
        return "%s %s %s %s" % (self.used_at,self.stock_in.product.name,self.unit_used,self.stock_in.product.base_unit)

    class Meta:
        ordering = ['-lastmodification']
        
class ReturningProduct(models.Model):
    date_return = models.DateField(verbose_name=_("Date return"),auto_now_add=True)
    using_product = models.ForeignKey(UsingProduct, on_delete=models.PROTECT)
    unit_return = models.IntegerField(default=1)
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby =  CurrentUserField()
    history = HistoricalRecords()
    
    def get_absolute_url(self):
        return reverse('usingproduct_detail', args=[str(self.id)])
    
    def __str__(self):
        return "%s %s %s %s" % (self.using_product.used_at,self.using_product.stock_in.product.name,self.unit_return,self.using_product.stock_in.product.base_unit)

    class Meta:
        ordering = ['-lastmodification']
    