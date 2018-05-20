# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django.conf import settings
from datetime import datetime, date

from billing.models import Orders,SuperGroups,Tests,OrderTests,Genders,OrderSamples


class ReceivedSamples(models.Model):
    order =  models.ForeignKey(Orders,on_delete=models.PROTECT,verbose_name=_("Order"),related_name='receivedsamples_order')
    sample =  models.ForeignKey(OrderSamples,on_delete=models.PROTECT,verbose_name=_("Specimen"),related_name='receivedsamples_tube')
    supergroup = models.ForeignKey(SuperGroups,on_delete=models.PROTECT,verbose_name=_("Super Group"),related_name='receivedsamples_supergrup')
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def __str__(self):
        return "%s%s" % (self.order.number,self.suffix)

class Instruments(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Name"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def __str__(self):
        return "%s" % (self.name)

AGE_UNIT = (
    ('D','DAY'),
    ('M','MONTH'),
    ('Y','YEAR')
    )
REF_OPERATOR = (
    ('-','NA'),
    ('>','GT'),
    ('>=','GTE'),
    ('<','LT'),
    ('<=','LTE'),
    )
    
class TestRefRanges(models.Model):
    DAY = 'D'
    MONTH = 'M'
    YEAR = 'Y'
    NA ='-'
    GT = '>'
    GTE = '>='
    LT = '<'
    LTE = '<='
    test = models.ForeignKey(Tests,on_delete=models.PROTECT,verbose_name=_("Test"),related_name='refranges_test')
    gender = models.ForeignKey(Genders,on_delete=models.PROTECT,verbose_name=_("Gender"),related_name='refranges_gender',blank=True,null=True)
    age_from = models.IntegerField(verbose_name=_("Age from"), null=True,blank=True)
    age_type =  models.CharField(
        max_length=3,
        verbose_name=_("Age from unit"),
        choices=AGE_UNIT,
        null=True,
        blank=True,
    )
    age_to = models.IntegerField(verbose_name=_("Age to"), null=True,blank=True)
    age_type =  models.CharField(
        max_length=3,
        verbose_name=_("Age to unit"),
        choices=AGE_UNIT,
        null=True,
        blank=True,
    )
    operator = models.CharField(
        max_length=3,
        verbose_name=_("Operator"),
        choices=REF_OPERATOR,
        null=True,
        blank=True,
    )
    any_age = models.BooleanField(verbose_name=_("Any age?"), default=True,blank=True)
    lower = models.IntegerField(verbose_name=_("lower limit"), null=True,blank=True)
    upper = models.IntegerField(verbose_name=_("upper limit"), null=True,blank=True)
    operator_value = models.IntegerField(verbose_name=_("operator value"), null=True,blank=True)
    alfa_value = models.CharField(max_length=100,verbose_name=_("Alfanumberic value"),null=True,blank=True)
    special_info = models.TextField(verbose_name=_("Special information"),null=True,blank=True)

    
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def __str__(self):
        return "%s" % (self.test)
    
    
    
class Results(models.Model):
    order =  models.ForeignKey(Orders,on_delete=models.PROTECT,verbose_name=_("Order"),related_name='results_order')
    test = models.ForeignKey(Tests,on_delete=models.PROTECT,verbose_name=_("Test"),related_name='results_test')
    numeric_result = models.FloatField(verbose_name=_("Numeric result"),null=True)
    alfa_result = models.CharField(max_length=100,verbose_name=_("Alfanumeric result"),null=True)
    text_result = models.TextField(verbose_name=_("Text result"),null=True)
    image_result = models.BinaryField(verbose_name=_("Image result"),null=True)
    ref_range = models.CharField(max_length=100,verbose_name=_("Reference range"),null=True)
    mark = models.CharField(max_length=3,verbose_name=_("Result mark"),null=True)
    instrument =  models.ForeignKey(Instruments,on_delete=models.PROTECT,verbose_name=_("Instrument"),related_name='results_instrument',null=True)
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False
        
    def get_patient_age_in_day(self):
        return (self.order.order_date - self.order.patient.dob).days
             
    def setup_range(self,alfa_value=None,operator=None,operator_value=None,lower=None,upper=None):
        if alfa_value:
            self.ref_range = alfa_value
            if self.alfa_result <> str(alfa_value):
                self.mark = 'A'
        else:
            # numeric range
            if operator:
                self.ref_range = str(operator)+' '+str(operator_value)
                if self.is_number(self.alfa_result):
                    # GT
                    if str(operator)=='>':
                        if float(self.alfa_result)<=float(operator_value):
                            self.mark = 'L'
                    if str(operator)=='>=':
                        if float(self.alfa_result)<float(operator_value):
                            self.mark = 'L'
                    if str(operator)=='<':
                        if float(self.alfa_result)>=float(operator_value):
                            self.mark = 'H'
                    if str(operator)=='<=':
                        if float(self.alfa_result)>float(operator_value):
                            self.mark = 'H'
            else:
                # range
                self.ref_range = str(lower)+' - '+str(upper)
                if self.alfa_result:
                    if self.is_number(self.alfa_result):
                        if float(self.alfa_result)<float(lower):
                            self.mark = 'L'
                        if float(self.alfa_result)>float(upper):
                            self.mark = 'H'
                     
   
    def save(self, *args, **kwargs):
        refrange = TestRefRanges.objects.filter(test=self.test).values('any_age','gender','age_type','age_from','age_to','operator','operator_value','lower','upper','alfa_value','special_info','gender_id')
        if refrange.count()>0:
            for range in refrange:
                # any age & any gender
                if range['any_age']:
                    # check gender
                    if not range['gender']:
                        self.setup_range(alfa_value=range['alfa_value'],
                                         operator=range['operator'],
                                         operator_value=range['operator_value'],
                                         lower=range['lower'],
                                         upper=range['upper'])
                                        
                    else:
                        # gender set
                        if range['gender'] == self.order.patient.gender_id:
                            self.setup_range(alfa_value=range['alfa_value'],
                                         operator=range['operator'],
                                         operator_value=range['operator_value'],
                                         lower=range['lower'],
                                         upper=range['upper'])
                else:
                    # date range
                    # Days
                    if range['age_type']=='D':
                        #print str((self.order.order_date - self.order.patient.dob).days)
                        if int(range['age_from']) <= (self.order.order_date - self.order.patient.dob).days <= int(range['age_to']):
                            if (not range['gender']) or (range['gender'] == self.order.patient.gender_id) :
                                self.setup_range(alfa_value=range['alfa_value'],
                                         operator=range['operator'],
                                         operator_value=range['operator_value'],
                                         lower=range['lower'],
                                         upper=range['upper'])
                    # Months
                    if range['age_type']=='M':
                        if int(range['age_from']) <= (self.order.order_date - self.order.patient.dob).months <= int(range['age_to']):
                            if (not range['gender']) or (range['gender'] == self.order.patient.gender_id) :
                                self.setup_range(alfa_value=range['alfa_value'],
                                         operator=range['operator'],
                                         operator_value=range['operator_value'],
                                         lower=range['lower'],
                                         upper=range['upper'])
                    # Years
                    if range['age_type']=='Y':
                        if int(range['age_from']) <= (self.order.order_date - self.order.patient.dob).months <= int(range['age_to']):
                            if (not range['gender']) or (range['gender'] == self.order.patient.gender_id) :
                                self.setup_range(alfa_value=range['alfa_value'],
                                         operator=range['operator'],
                                         operator_value=range['operator_value'],
                                         lower=range['lower'],
                                         upper=range['upper'])
                                
                            
                #print range
        
        super(Results, self).save(*args, **kwargs)
    
    def __str__(self):
        return "%s %s %s %s" % (self.order,self.numeric_result,self.alfa_result,self.text_result)
    
class TestParameters(models.Model):
    test = models.OneToOneField(Tests,on_delete=models.CASCADE,primary_key=True,)
    method = models.CharField(max_length=100,verbose_name=_("Method"),null=True)
    unit = models.CharField(max_length=100,verbose_name=_("Test unit"),null=True)
    decimal = models.IntegerField(verbose_name=_("Decimal place"),null=True)
    
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def __str__(self):
        return "%s" % (self.test)


class OrderResults(models.Model):
    order =  models.ForeignKey(Orders,on_delete=models.PROTECT,verbose_name=_("Order"),related_name='orderresults_order')
    test = models.ForeignKey(Tests,on_delete=models.PROTECT,verbose_name=_("Test"),related_name='orderresults_test')
    is_header = models.BooleanField(default=False,verbose_name=_("is header?"))
    result = models.ForeignKey(Results,on_delete=models.PROTECT,verbose_name=_("Result"),related_name='orderresults_result',null=True)
    unit = models.CharField(max_length=100,verbose_name=_("Result unit"),null=True)
    ref_range = models.CharField(max_length=200,verbose_name=_("Reference range"),null=True)
    patologi_mark = models.CharField(max_length=2,verbose_name=_("Patologi mark"),null=True)
    validation_status = models.IntegerField(verbose_name=_("Validation status"),default=0)
    validation_user = models.CharField(max_length=20,verbose_name=_("Validated by"),null=True)
    validation_date = models.DateTimeField(verbose_name=_("Validated date"),null=True)
    print_status = models.IntegerField(verbose_name=_("Print status"),default=0)
    print_user = models.CharField(max_length=20,verbose_name=_("Print by"),null=True)
    print_date = models.DateTimeField(verbose_name=_("Print date"),null=True)
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def __str__(self):
        return "%s %s %s" % (self.order,self.test,self.result)
    
    