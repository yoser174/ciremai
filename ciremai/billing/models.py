from __future__ import unicode_literals

from django.db import models
from django.db.models import ExpressionWrapper,F,Sum,DecimalField
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
import datetime
from datetime import date
from collections import defaultdict
from num2words import num2words
from django.db.models.signals import pre_save,post_save,post_delete
from django.dispatch import receiver
from decimal import *


def float_to_decimal(f):
    "Convert a floating point number to a Decimal with no loss of information"
    n, d = f.as_integer_ratio()
    numerator, denominator = Decimal(n), Decimal(d)
    ctx = Context(prec=60)
    result = ctx.divide(numerator, denominator)
    while ctx.flags[Inexact]:
        ctx.flags[Inexact] = False
        ctx.prec *= 2
        result = ctx.divide(numerator, denominator)
    return result


class Parameters(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Name"))
    char_value = models.CharField(max_length=100,verbose_name=_("Char value"),null=True,blank=True)
    num_value = models.IntegerField(verbose_name=_("Numeric value"),null=True,blank=True)
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('parameters_detail', args=[str(self.id)])
    
    def __str__(self):
        return "%s %s %s" % (self.name,self.char_value,self.num_value)

    class Meta:
        verbose_name = _("Parameter")
        verbose_name_plural = _("Parameters")

class Priority(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Group Name"))
    ext_code = models.CharField(max_length=30,verbose_name=_("External code"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('priority_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Priority")
        verbose_name_plural = _("Priorities")
        
class Insurance(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Insurence Name"))
    ext_code = models.CharField(max_length=30,verbose_name=_("External code"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('insurence_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Insurence")
        verbose_name_plural = _("Insurences")
        
class Doctors(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Doctor Name"))
    ext_code = models.CharField(max_length=30,verbose_name=_("External code"))
    address = models.CharField(max_length=100,verbose_name=_("Address"),help_text=_("Doctor Address"),null=True,blank=True)
    phone = models.CharField(max_length=100,verbose_name=_("Mobile"),help_text=_("Mobile"),null=True,blank=True)
    mobile = models.CharField(max_length=100,verbose_name=_("Phone"),help_text=_("Phone"),null=True,blank=True)
    email = models.EmailField(verbose_name=_("e-mail"),null=True,blank=True)
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('doctors_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")
        
class Origins(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Origin Name"))
    ext_code = models.CharField(max_length=30,verbose_name=_("External code"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('origins_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Origin")
        verbose_name_plural = _("Origins")
        
        
class Diagnosis(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Diangosis Name"))
    ext_code = models.CharField(max_length=30,verbose_name=_("External code"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('diagnosis_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Diagnosis")
        verbose_name_plural = _("Diagnosis")
        
class Genders(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Gender Name"))
    ext_code = models.CharField(max_length=30,verbose_name=_("External code"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('priority_detail', args=[str(self.id)])
    
    def __str__(self):
        return ('%s (%s)' % (self.name,self.ext_code))

    class Meta:
        verbose_name = _("Gender")
        verbose_name_plural = _("Genders")
        
        
class Specimens(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Specimen Name"))
    suffix_code = models.CharField(max_length=3,verbose_name=_("Suffix code"))
    
    def get_absolute_url(self):
        return reverse('specimen_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Specimen")
        verbose_name_plural = _("Specimens")
        
class SuperGroups(models.Model):
    abbreviation = models.CharField(max_length=100,verbose_name=_("Abbreviation"))
    name = models.CharField(max_length=100,verbose_name=_("Name"))
    
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def __str__(self):
        return "%s %s" % (self.abbreviation,self.name)

class TestGroups(models.Model):
    supergroup = models.ForeignKey(SuperGroups,on_delete=models.PROTECT,verbose_name=_("Super Group"),related_name='testgroup_supergroup',null=True)
    name = models.CharField(max_length=100,verbose_name=_("Group Name"))
    sort = models.IntegerField(verbose_name=_("Sort"),help_text=_("Sorted priority"))
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('testgroups_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Test group")
        verbose_name_plural = _("Test groups")
        permissions = (
            ('view_testgroups', 'Can view testgroups'),
        )
        ordering = ['name']
        
        
TEST_RESULT_TYPE = (
    ('NUM','NUMERIC'),
    ('ALF','ALFANUMERIC'),
    ('TXT','TEXT'),
    ('IMG','IMAGE')
    )        
class Tests(models.Model):
    NUMERIC = 'NUM'
    ALFANUMERIC = 'ALF'
    TEXT = 'TXT'
    IMAGE = 'IMG'
    test_group = models.ForeignKey(TestGroups,on_delete=models.PROTECT,verbose_name=_("Test Group"),related_name='tests')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    name = models.CharField(max_length=100,verbose_name=_("Test Name"),null=True)
    result_type =  models.CharField(
        max_length=3,
        verbose_name=_("Result Type"),
        choices=TEST_RESULT_TYPE,
        default=NUMERIC,
    )
    is_active = models.BooleanField(verbose_name=_("is active?"), default=True,blank=True)
    specimen = models.ForeignKey(Specimens,on_delete=models.PROTECT,verbose_name=_("Specimen"),related_name='test_specimen',null=True)
    can_request = models.BooleanField(verbose_name=_("Can request?"), default=True,blank=True)
    sort = models.IntegerField(verbose_name=_("Sort"),help_text=_("Sorted priority"))
    ext_code = models.CharField(max_length=30,verbose_name=_("External code"))
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('tests_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Tests")
        permissions = (
            ('view_tests', 'Can view tests'),
        )
        ordering = ['test_group','name']
    
    
    
class TestPrices(models.Model):
    test = models.OneToOneField(Tests,on_delete=models.PROTECT,verbose_name=_("Test"),related_name='test_price')
    tariff = models.DecimalField(decimal_places=2, max_digits=20,verbose_name=_("tariff"),help_text=_("base tariff"))
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('testprices_detail', args=[str(self.id)])
    
    def __str__(self):
        return '%s %s' % (self.test,self.priority)

    class Meta:
        verbose_name = _("Test price")
        verbose_name_plural = _("Test prices")
        permissions = (
            ('view_testprices', 'Can view test prices'),
        )
        ordering = ['test']
        #unique_together = ("test", "is_active")
 
 
class Salutation(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Salutation"),null=True)
    
    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name = _("Salutation")
        verbose_name_plural = _("Salutations")
           

def auto_patient_id():
        dtf = datetime.datetime.today().strftime('%y')
        par = Parameters.objects.filter(name='PATIENT_ID',char_value=dtf)
        if par.count()==0:
            Parameters.objects.filter(name='PATIENT_ID').delete()
            par = Parameters(name='PATIENT_ID',char_value=dtf,num_value=1)
            par.save()
        par = Parameters.objects.filter(name='PATIENT_ID',char_value=dtf)
        id = par.values('id')[0]['id']
        num_value = int(par.values('num_value')[0]['num_value'])
        par_upd = Parameters.objects.get(pk=id)
        par_upd.num_value=num_value+1
        par_upd.save()
        return '001' + dtf + ("%05d" % (num_value,))
         
class Patients(models.Model):
    patient_id = models.CharField(max_length=100,verbose_name=_("Patient ID"),default=auto_patient_id,blank=True,null=True,unique=True)
    salutation = models.ForeignKey(Salutation,on_delete=models.PROTECT,verbose_name=_("Salutation"),null=True,blank=True)
    name = models.CharField(max_length=100,verbose_name=_("Name"),help_text=_("Patient Name"))
    gender = models.ForeignKey(Genders,on_delete=models.PROTECT,verbose_name=_("Gender"))
    dob = models.DateField(verbose_name=_("Date of birth"),help_text=_("Date format: DD-MM-YYYY"))
    address = models.CharField(max_length=1000,verbose_name=_("Address"),help_text=_("Patient Address"))
    phone = models.CharField(max_length=100,verbose_name=_("Mobile"),help_text=_("Mobile"),null=True,blank=True)
    mobile = models.CharField(max_length=100,verbose_name=_("Phone"),help_text=_("Phone"),null=True,blank=True)
    email = models.EmailField(verbose_name=_("e-mail"),null=True,blank=True)
    data0 = models.CharField(max_length=100,verbose_name=_("Data 0"),help_text=_("Additional data 0"),blank=True,null=True)
    data1 = models.CharField(max_length=100,verbose_name=_("Data 1"),help_text=_("Additional data 1"),blank=True,null=True)
    data2 = models.CharField(max_length=100,verbose_name=_("Data 2"),help_text=_("Additional data 3"),blank=True,null=True)
    note = models.TextField(verbose_name=_("Note"),null=True,blank=True)
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"),null=True)
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True) 
    
    def get_absolute_url(self):
        return reverse('patient_detail', args=[str(self.id)])
    
    def calculate_age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    
    def create_order(self):
        order = Orders(patient=self)
        #order.doctor_id = 1
        #order.origin_id = 1
        #order.insurence_id = 1
        #order.priority_id = 1
        #order.lastmodifiedby_id = 1
        order.save()
        return order
    
    def __str__(self):
        return '%s %s' % (self.patient_id,self.name)

    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
        permissions = (
            ('view_patients', 'Can view test patients'),
        )
        ordering = ['patient_id','name']
        
def auto_order_no():
        dtf = datetime.datetime.today().strftime('%y%m%d')
        par = Parameters.objects.filter(name='ORDER_NO',char_value=dtf)
        if par.count()==0:
            Parameters.objects.filter(name='ORDER_NO').delete()
            par = Parameters(name='ORDER_NO',char_value=dtf,num_value=1)
            par.save()
        par = Parameters.objects.filter(name='ORDER_NO',char_value=dtf)
        id = par.values('id')[0]['id']
        num_value = int(par.values('num_value')[0]['num_value'])
        par_upd = Parameters.objects.get(pk=id)
        par_upd.num_value=num_value+1
        par_upd.save()
        return '1' + dtf + ("%04d" % (num_value,))

ORDER_STATUS = (('0', 'Draft'),
                ('1', 'Already Paid'),
                ('9', 'Other'))
    
class Orders(models.Model):
    status = models.CharField(
        max_length=3,
        verbose_name=_("Status"),
        choices=ORDER_STATUS,
        default=0,
    )
    order_date = models.DateField(verbose_name=_("Order date"),auto_now_add=True)
    number = models.CharField(max_length=100,verbose_name=_("Number"),default=auto_order_no,blank=True,null=True,unique=True)
    origin = models.ForeignKey(Origins,on_delete=models.PROTECT,verbose_name=_("Origin"),null=True,blank=True)
    doctor = models.ForeignKey(Doctors,on_delete=models.PROTECT,verbose_name=_("Sender doctor"),null=True,blank=True)
    diagnosis = models.ForeignKey(Diagnosis,on_delete=models.PROTECT,verbose_name=_("Diagnosis"),null=True,blank=True)
    priority = models.ForeignKey(Priority,on_delete=models.PROTECT,verbose_name=_("Order priority"),null=True,blank=True)
    #insurance = models.ForeignKey(Insurance,on_delete=models.PROTECT,verbose_name=_("Insurance"),null=True,blank=True)
    note = models.CharField(max_length=100,verbose_name=_("Note/Comment"),blank=True,null=True)
    discount = models.FloatField(verbose_name=_("Discount"),blank=True,null=True,default=0)
    discount_amount = models.FloatField(verbose_name=_("Discount amount"),blank=True,null=True,default=0)
    payment = models.FloatField(verbose_name=_("Payment amount"),blank=True,null=True)
    patient = models.ForeignKey(Patients,on_delete=models.PROTECT,verbose_name=_("Patient"))
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"),auto_now_add=True)
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    #objects = OrdersManager()
    
    def has_tests(self):
        if OrderTests.objects.filter(order_id=self.pk).count() > 0:
            return True
        else:
            return False
    
    def get_tests(self):
        return Orders.objects.filter(pk=self.pk).values_list(
                                         'order_items__test__name',flat=True)
    
    def get_test_str(self):
        order_result = Orders.objects.filter(pk=self.pk,
                                     order_items__test__test_price__priority=self.priority).values_list(
                                         'order_items__test__name',flat=False)
        data = [entry[0] for entry in order_result]
        return ", ".join(map(str,data))
                            
                                     
    def get_test_price(self):
        return Orders.objects.filter(pk=self.pk).values(
            'order_items__test__id',
            'order_items__test__test_group__name',
            'order_items__test__name',
            'order_items__test__test_price__tariff').annotate(
                sub_total=ExpressionWrapper(F('order_items__test__test_price__tariff'),
                                            output_field=DecimalField(decimal_places=2) )
                                                            )
    def get_total_price(self):
        print self.get_sub_total_price()['subtotal']
        print float(self.discount_amount)
        ordertest = OrderTests.objects.filter(order=self.pk)
        if ordertest.count()>0:
            total = (float(self.get_sub_total_price()['subtotal']) - float(self.discount_amount))
            
        else:
            total = 0
            
        total = Decimal.from_float(total)

        print "Total %s" % total
        return total
    
    def get_sub_total_price(self):
        return Orders.objects.filter(pk=self.pk).aggregate(
                                         subtotal=Sum(F('order_items__test__test_price__tariff')))
                                            
    def get_sub_total_price_tariff(self):
        return Orders.objects.filter(pk=self.pk).aggregate(
                                         tariff_subtotal=Sum(F('order_items__test__test_price__tariff'))
                                         ).values()[0]
    def get_sub_total_price_service(self):
        return Orders.objects.filter(pk=self.pk).aggregate(
                                         tariff_subtotal=0).values()[0]
                                                                      
    def get_total_price_words(self):
        return num2words(int(self.get_total_price()),lang='id')
    
    def get_absolute_url(self):
        return reverse('orders_detail', args=[str(self.id)])
        
    def __str__(self):
        return '%s %s' % (self.number,self.patient)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        permissions = (
            ('view_orders', 'Can view orders'),
        )
        ordering = ['number','origin']

class OrderTests(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.PROTECT,verbose_name=_("Order"),related_name='order_items')
    test = models.ForeignKey(Tests,on_delete=models.PROTECT,verbose_name=_("Test"),related_name='order_tests')
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"),auto_now_add=True)
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('ordertests_detail', args=[str(self.id)])
    
    def __str__(self):
        return '%s %s' % (self.order,self.test)

    class Meta:
        verbose_name = _("Order test")
        verbose_name_plural = _("Order tests")
        permissions = (
            ('view_ordertests', 'Can view order tests'),
        )
        ordering = ['order','test']

class OrderSamples(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.PROTECT,verbose_name=_("Order"),related_name='sample_order')
    specimen = models.ForeignKey(Specimens,on_delete=models.PROTECT,verbose_name=_("Specimen"),related_name='sample_specimen')
    sample_no = models.CharField(max_length=100,verbose_name=_("sample id"),help_text=_("Sample id"))
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"),auto_now_add=True)
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('ordersamples_detail', args=[str(self.id)])
    
    def __str__(self):
        return '%s' % (self.sample_no)

    class Meta:
        verbose_name = _("Order samples")
        verbose_name_plural = _("Order samples")
        permissions = (
            ('view_ordersamples', 'Can view order samples'),
        )
        ordering = ['order','sample_no']
        
class LabelPrinters(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Name"),help_text=_("Printer barcode name"))
    active = models.BooleanField(default=True,verbose_name=_("is active?"))
    com_port = models.CharField(max_length=100,verbose_name=_("Com serial port name"),help_text=_("eq: COM10,COM11"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def get_absolute_url(self):
        return reverse('ordersamples_detail', args=[str(self.id)])
    
    def __str__(self):
        return '%s (%s)' % (self.name,self.com_port)
    
    
PAYMENT_TYPE = ((0, 'Cash'),
                (1, 'Debit/Credit Card'),
                (9, 'Other'))
class OrderPayments(models.Model):
    order = models.OneToOneField(Orders,on_delete=models.PROTECT,verbose_name=_("Order"),related_name='order_payment')
    type = models.CharField(
        max_length=3,
        verbose_name=_("Payment Type"),
        choices=PAYMENT_TYPE,
        default=0,
    )
    #amount = models.DecimalField(verbose_name=_('Amount'),decimal_places=2, max_digits=20,default=0,null=True)
    
    def __str__(self):
        return '%s (%s) %s' % (self.order,self.type, self.amount)
    
    
    
################ SIGNAL ############################
@receiver(post_save, sender=OrderTests)
def ordertest_signal(sender , instance , **kwargs):
    #if kwargs.get('created'):
    #    return
    order = Orders.objects.get(pk=instance.order_id)
    print 'ordertest signal...'
    try:
        print float(order.get_sub_total_price()['subtotal'])
        print order.discount
        disc_amount = float(order.get_sub_total_price()['subtotal']) * float(order.discount) / 100
        print disc_amount
        print order.discount_amount
    except:
        return
    if order.discount_amount <> disc_amount:
        order.discount_amount = disc_amount
        order.save()
    return

@receiver(post_delete, sender=OrderTests)
def ordertest_signal(sender , instance , **kwargs):
    #if kwargs.get('created'):
    #    return
    order = Orders.objects.get(pk=instance.order_id)
    print 'ordertest signal...'
    try:
        print float(order.get_sub_total_price()['subtotal'])
        print order.discount
        disc_amount = float(order.get_sub_total_price()['subtotal']) * float(order.discount) / 100
        print disc_amount
        print order.discount_amount
    except:
        return
    if order.discount_amount <> disc_amount:
        order.discount_amount = disc_amount
        order.save()
    return


@receiver(post_save, sender=Orders)
def hear_signal(sender , instance , **kwargs):
    if kwargs.get('created'):
        return # if a new model object is created then return. You need to distinguish between a new object created and the one that just got updated.
    
    
    print 'signal save....'

    try:
        print 'calculate discount'
        print instance.get_sub_total_price()['subtotal']
        print instance.discount
        disc_amount = float(instance.get_sub_total_price()['subtotal']) * float(instance.discount) / 100
        print disc_amount
    except:
        print 'gagal exception'
        disc_amount = 0
        
    print 'discount_amount_calc' + str(disc_amount)
    print instance.discount_amount
    if instance.discount_amount <> disc_amount:
        print 'tidak sama'
        instance.discount_amount = disc_amount
        instance.save()
    return
    
    
############ TESTING MODEL ########################
class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    article_heading = models.CharField(max_length=250)
    article_body = models.TextField()
    
    