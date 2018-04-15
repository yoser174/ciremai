# coding=utf-8
from datetimewidget.widgets import DateWidget
from django import forms
from crispy_forms.helper import FormHelper
from .models import Product,StockIn,StockInLot,UsingProduct,ReturningProduct



class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        #exclude = ()
        fields = ('number','name','active','supplier','base_unit','lot_controlled','temperature_condition','vendor','lead_time')
        
class StockinForm(forms.ModelForm):
    
    class Meta:
        model = StockIn
        #exclude = ()
        fields = ('supplier','storage','product','supplier','quantity')
        #widgets = {
        #    'publish_date': forms.DateTimeInput()
        #}

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