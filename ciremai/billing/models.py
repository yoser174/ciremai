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



class Parameters(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Name"))
    char_value = models.CharField(max_length=100,verbose_name=_("Char value"))
    num_value = models.IntegerField(verbose_name=_("Numeric value"))
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
        return self.name

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
    specimen = models.ForeignKey(Specimens,on_delete=models.PROTECT,verbose_name=_("Specimen"),related_name='test_specimen',null=True)
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
    test = models.ForeignKey(Tests,on_delete=models.PROTECT,verbose_name=_("Test"),related_name='test_price')
    priority = models.ForeignKey(Priority,on_delete=models.PROTECT,verbose_name=_("Priority"))
    tariff = models.DecimalField(decimal_places=2, max_digits=20,verbose_name=_("tariff"),help_text=_("base tariff"))
    service = models.DecimalField(decimal_places=2, max_digits=20,verbose_name=_("Medc.Serv"),help_text=_("Medical service rate"))
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
        ordering = ['test','priority']
        
class Patients(models.Model):
    patient_id = models.CharField(max_length=100,verbose_name=_("Patient ID"),help_text=_("Medical record number"),unique=True)
    name = models.CharField(max_length=100,verbose_name=_("Name"),help_text=_("Patient Name"))
    gender = models.ForeignKey(Genders,on_delete=models.PROTECT,verbose_name=_("Gender"))
    dob = models.DateField(verbose_name=_("Date of birth"),help_text=_("Date format: DD-MM-YYYY"))
    address = models.CharField(max_length=100,verbose_name=_("Address"),help_text=_("Patient Address"))
    data0 = models.CharField(max_length=100,verbose_name=_("Data 0"),help_text=_("Additional data 0"),blank=True,null=True)
    data1 = models.CharField(max_length=100,verbose_name=_("Data 1"),help_text=_("Additional data 1"),blank=True,null=True)
    data2 = models.CharField(max_length=100,verbose_name=_("Data 2"),help_text=_("Additional data 3"),blank=True,null=True)
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
        order.doctor_id = 1
        order.origin_id = 1
        order.insurence_id = 1
        order.priority_id = 1
        order.lastmodifiedby_id = 1
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
        return dtf + ("%04d" % (num_value,))
    
#class OrdersManager(models.Manager):
#    def get_test_with_price(self,id):
#        from django.db import connection
#        with connection.cursor() as cursor:
#            cursor.execute("""
#            SELECT t.name,tp.tariff, tp.service,tp.tariff + tp.service subtotal
#            FROM billing_orders o
#            LEFT JOIN billing_ordertests ot ON o.id = ot.order_id
#            LEFT JOIN billing_tests t ON ot.test_id = t.id
#            LEFT JOIN billing_testprices tp oN t.id = tp.test_id AND tp.priority_id = o.priority_id
#            WHERE o.id = %s
#            ORDER BY ot.id """,id)
#            result_list = cursor.fetchall()
#        return result_list
    
class Orders(models.Model):
    order_date = models.DateField(verbose_name=_("Order date"),auto_now_add=True)
    number = models.CharField(max_length=100,verbose_name=_("Number"),default=auto_order_no,blank=True,null=True,unique=True)
    origin = models.ForeignKey(Origins,on_delete=models.PROTECT,verbose_name=_("Origin"))
    doctor = models.ForeignKey(Doctors,on_delete=models.PROTECT,verbose_name=_("Sender doctor"))
    diagnosis = models.ForeignKey(Diagnosis,on_delete=models.PROTECT,verbose_name=_("Diagnosis"),null=True,blank=True)
    priority = models.ForeignKey(Priority,on_delete=models.PROTECT,verbose_name=_("Order priority"),null=True,blank=True)
    insurance = models.ForeignKey(Insurance,on_delete=models.PROTECT,verbose_name=_("Insurance"),null=True,blank=True)
    note = models.CharField(max_length=100,verbose_name=_("Note/Comment"),blank=True,null=True)
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
        return Orders.objects.filter(pk=self.pk,
                                     order_items__test__test_price__priority=self.priority).values_list(
                                         'order_items__test__name',flat=True)
    
    def get_test_str(self):
        order_result = Orders.objects.filter(pk=self.pk,
                                     order_items__test__test_price__priority=self.priority).values_list(
                                         'order_items__test__name',flat=False)
        data = [entry[0] for entry in order_result]
        return ", ".join(map(str,data))
                            
                                     
    def get_test_price(self):
        return Orders.objects.filter(pk=self.pk,
                                     order_items__test__test_price__priority=self.priority).values(
                                         'order_items__test__name',
                                         'order_items__test__test_price__tariff',
                                         'order_items__test__test_price__service').annotate(
                                             sub_total=ExpressionWrapper(
                                                 F('order_items__test__test_price__tariff') + F('order_items__test__test_price__service'),
                                                 output_field=DecimalField(decimal_places=2) )
                                                                                            )
    def get_total_price(self):
        return Orders.objects.filter(pk=self.pk,
                                     order_items__test__test_price__priority=self.priority).aggregate(
                                         total=Sum(F('order_items__test__test_price__tariff')
                                                   +F('order_items__test__test_price__service'))
                                         )
    def get_sub_total_price(self):
        return Orders.objects.filter(pk=self.pk,
                                     order_items__test__test_price__priority=self.priority).aggregate(
                                         tariff_subtotal=Sum(F('order_items__test__test_price__tariff')),
                                         service_subtotal=Sum(F('order_items__test__test_price__service'))
                                         )   
    def get_sub_total_price_tariff(self):
        return Orders.objects.filter(pk=self.pk,
                                     order_items__test__test_price__priority=self.priority).aggregate(
                                         tariff_subtotal=Sum(F('order_items__test__test_price__tariff'))
                                         ).values()[0]
    def get_sub_total_price_service(self):
        return Orders.objects.filter(pk=self.pk,
                                     order_items__test__test_price__priority=self.priority).aggregate(
                                         tariff_subtotal=Sum(F('order_items__test__test_price__service'))
                                         ).values()[0]
                                                                      
    def get_total_price_words(self):
        return num2words(int(self.get_total_price()['total']),lang='id')
    
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
    sample_no = models.CharField(max_length=100,verbose_name=_("Name"),help_text=_("Patient Name"))
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
    