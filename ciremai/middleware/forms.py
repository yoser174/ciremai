from django import forms
from .models import ReceivedSamples

class ReceivedSamplesForm(forms.ModelForm):
    class Meta:
        model = ReceivedSamples
        fields = ('order','supergroup')