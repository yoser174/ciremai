# coding=utf-8
from datetimewidget.widgets import DateWidget
from django import forms
from crispy_forms.helper import FormHelper
from .models import Product,StockIn,StockInLot,UsingProduct,ReturningProduct,Storage,Unit

from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)



class ProductForm(forms.ModelForm):
    
    
    class Meta:
        model = Product
        #exclude = ()
        fields = ('number','name','supplier','unit','base_multiplier','base_unit','lot_controlled','temperature_condition','vendor','lead_time')
        
class StockinForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=Select2Widget)
    storage = forms.ModelChoiceField(queryset=Storage.objects.all(), widget=Select2Widget)
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), widget=Select2Widget)
    
    class Meta:
        model = StockIn
        fields = ('product','quantity','unit','storage',)

class StockinLotForm(forms.ModelForm):
    
    class Meta:
        model = StockInLot
        fields = ('number','expired')
        
        
    def __init__(self, *args, **kwargs):
        super(StockinLotForm, self).__init__(*args, **kwargs)
        self.fields['expired'] = forms.DateField(widget=DateWidget(bootstrap_version=3, usel10n=True))
        self.helper = FormHelper()
        self.helper.form_tag = False

class UsingProductForm(forms.ModelForm):
    
    class Meta:
        model = UsingProduct
        fields = ('used_at','unit_used',)
        
class ReturningProductForm(forms.ModelForm):
    
    class Meta:
        model = ReturningProduct
        fields = ('unit_return',)