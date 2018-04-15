# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django.conf import settings

from billing.models import Orders,SuperGroups,Tests

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
    
class OrderResults(models.Model):
    order =  models.ForeignKey(Orders,on_delete=models.PROTECT,verbose_name=_("Order"),related_name='orderresults_order')
    test = models.ForeignKey(Tests,on_delete=models.PROTECT,verbose_name=_("Test"),related_name='orderresults_test')
    result = models.ForeignKey(Results,on_delete=models.PROTECT,verbose_name=_("Result"),related_name='orderresults_result',null=True)
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    
    def __str__(self):
        return "%s %s %s" % (self.order,self.test,self.result)
    
    