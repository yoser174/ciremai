# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django.conf import settings

from billing.models import Orders,SuperGroups,Tests,OrderTests,Genders

class Specimens(models.Model):
    abbreviation = models.CharField(max_length=100,verbose_name=_("Abbreviation"))
    name = models.CharField(max_length=100,verbose_name=_("Name"))
    
    
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def __str__(self):
        return "%s %s" % (self.abbreviation,self.name)
    

class Tubes(models.Model):
    specimen = models.ForeignKey(Specimens,on_delete=models.PROTECT,verbose_name=_("Specimen"),related_name='tube_specimen')
    abbreviation = models.CharField(max_length=100,verbose_name=_("Abbreviation"))
    name = models.CharField(max_length=100,verbose_name=_("Name"))
    suffix = models.CharField(max_length=100,verbose_name=_("Suffix"))
    
    
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def __str__(self):
        return "%s %s" % (self.abbreviation,self.name)
    
    

class ReceivedSamples(models.Model):
    order =  models.ForeignKey(Orders,on_delete=models.PROTECT,verbose_name=_("Order"),related_name='receivedsamples_order')
    tube =  models.ForeignKey(Tubes,on_delete=models.PROTECT,verbose_name=_("Specimen"),related_name='receivedsamples_tube')
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
    
    
class Results(models.Model):
    order =  models.ForeignKey(Orders,on_delete=models.PROTECT,verbose_name=_("Order"),related_name='results_order')
    test = models.ForeignKey(Tests,on_delete=models.PROTECT,verbose_name=_("Test"),related_name='results_test')
    #order_test = models.ForeignKey(OrderTests,on_delete=models.PROTECT,verbose_name=_("Order test"),related_name='order_test')
    numeric_result = models.FloatField(verbose_name=_("Numeric result"),null=True)
    alfa_result = models.CharField(max_length=100,verbose_name=_("Alfanumeric result"),null=True)
    text_result = models.TextField(verbose_name=_("Text result"),null=True)
    image_result = models.BinaryField(verbose_name=_("Image result"),null=True)
    instrument =  models.ForeignKey(Instruments,on_delete=models.PROTECT,verbose_name=_("Instrument"),related_name='results_instrument',null=True)
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
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
    operator = models.IntegerField(verbose_name=_("operator value"), null=True,blank=True)
    alfa_value = models.CharField(max_length=100,verbose_name=_("Alfanumberic value"),null=True,blank=True)
    special_info = models.TextField(verbose_name=_("Special information"),null=True,blank=True)

    
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
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def __str__(self):
        return "%s %s %s" % (self.order,self.test,self.result)
    
    