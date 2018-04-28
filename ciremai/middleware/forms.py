from django import forms
from .models import ReceivedSamples,Results
from django.forms.models import inlineformset_factory
from billing.models import OrderTests

class ReceivedSamplesForm(forms.ModelForm):
    class Meta:
        model = ReceivedSamples
        fields = ('order','supergroup')
        
class OrderResultsForm(forms.ModelForm):
    class Meta:
        model = Results
        #fields = ('test',)
        exclude = ()
        

#OrderTestFormSet = inlineformset_factory(OrderTests,Results,form=OrderResultsForm, extra=1)