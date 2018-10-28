# coding=utf-8
from datetimewidget.widgets import DateWidget
from django import forms
from crispy_forms.helper import FormHelper
from .models import TestGroups,Tests,Patients,Orders,OrderTests,Origins,\
Insurance,Doctors,Diagnosis,Priority,Salutation, Genders,OrderPayments
from django.utils.translation import ugettext_lazy as _
from collections import OrderedDict as SortedDict

from itertools import groupby
from django.forms.models import (
    ModelChoiceIterator, ModelChoiceField, ModelMultipleChoiceField
)

from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)



class Grouped(object):
    def __init__(self, queryset, group_by_field,
                 group_label=None, *args, **kwargs):
        """ 
        ``group_by_field`` is the name of a field on the model to use as
                           an optgroup.
        ``group_label`` is a function to return a label for each optgroup.
        """
        super(Grouped, self).__init__(queryset, *args, **kwargs)
        self.group_by_field = group_by_field
        if group_label is None:
            self.group_label = lambda group: group
        else:
            self.group_label = group_label
   
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)


class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset.all()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for group, choices in groupby(self.queryset.all(),
                    key=lambda row: getattr(row, self.field.group_by_field)):
            if self.field.group_label(group):
                yield (
                    self.field.group_label(group),
                    [self.choice(ch) for ch in choices]
                )


class GroupedModelChoiceField(Grouped, ModelChoiceField):
    choices = property(Grouped._get_choices, ModelChoiceField._set_choices)


class GroupedModelMultiChoiceField(Grouped, ModelMultipleChoiceField):
    choices = property(Grouped._get_choices, ModelMultipleChoiceField._set_choices)

class TestGroupForm(forms.ModelForm):
    class Meta:
        model = TestGroups
        fields = ('name','sort')

class TestForm(forms.ModelForm):
    class Meta:
        model = Tests
        fields = ('test_group','name','sort')
        
class PatientForm(forms.ModelForm):
    ordered_field_names = ['patient_id','salutation','name','gender','age','dob','address','mobile','phone','email','note']
    
    salutation = forms.ModelChoiceField(queryset=Salutation.objects.all(), widget=Select2Widget,empty_label=None,required=False)
    gender = forms.ModelChoiceField(queryset=Genders.objects.all(), widget=Select2Widget,empty_label=None,required=True)
    age = forms.CharField(label=_("Age (year)"), max_length="4",required=False)
    
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        # Your field initialisation code
        self.rearrange_field_order()
    
    
    def rearrange_field_order(self):

        original_fields = self.fields
        new_fields = SortedDict()

        for field_name in self.ordered_field_names:
            field = original_fields.get(field_name)
            if field:
                new_fields[field_name] = field

        self.fields = new_fields
        
    class Meta:
        model = Patients
        fields = ('patient_id','salutation','name','gender','dob','address','mobile','phone','email','note')
        
    

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctors
        fields = ('name','address','mobile','phone','email')




class OrderForm2(forms.ModelForm):
    origin = forms.ModelChoiceField(queryset=Origins.objects.all(), widget=Select2Widget,empty_label=None)
    priority = forms.ModelChoiceField(queryset=Priority.objects.all(), widget=Select2Widget,empty_label=None)
    #insurance = forms.ModelChoiceField(queryset=Insurance.objects.all(), widget=Select2Widget,empty_label=None,required=False)
    doctor = forms.ModelChoiceField(queryset=Doctors.objects.all(), widget=Select2Widget,empty_label=None,required=False)
    diagnosis = forms.ModelChoiceField(queryset=Diagnosis.objects.all(),
                                       widget=Select2Widget,
                                       empty_label=None,
                                       required=False)
    #test_selections = forms.ModelMultipleChoiceField(queryset=Tests.objects.filter(can_request=True),
    #                                      widget=Select2MultipleWidget,
                                          #empty_label=None,
    #                                      required=False)
    def __init__(self, *args, **kwargs):
        super(OrderForm2, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        #if instance and instance.pk:
        #    self.fields['test_selections'].initial = list(Orders.objects.get(id=instance.pk).order_items.all().filter(test__can_request=True).values_list('test_id',flat=True).order_by('id'))
        
    class Meta:
        model = Orders
        fields = ('id','number','status','priority','origin','doctor','diagnosis','note')

class OrderForm(forms.ModelForm):
    origin = forms.ModelChoiceField(queryset=Origins.objects.all(), widget=Select2Widget,empty_label=None)
    priority = forms.ModelChoiceField(queryset=Priority.objects.all(), widget=Select2Widget,empty_label=None)
    insurance = forms.ModelChoiceField(queryset=Insurance.objects.all(), widget=Select2Widget,empty_label=None,required=False)
    doctor = forms.ModelChoiceField(queryset=Doctors.objects.all(), widget=Select2Widget,empty_label=None,required=False)
    diagnosis = forms.ModelChoiceField(queryset=Diagnosis.objects.all(),widget=Select2Widget,empty_label=None,required=False)
    test_selections =  GroupedModelMultiChoiceField(queryset = Tests.objects.filter(can_request=True), 
        group_by_field='test_group',
        widget  = forms.CheckboxSelectMultiple,
        )
    def __init__(self, *args, **kwargs):
        super(OrderForm2, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['number'].widget.attrs['readonly'] = True
            self.fields['test_selections'] = GroupedModelMultiChoiceField(queryset = Tests.objects.filter(can_request=True).order_by('sort'),
        group_by_field='test_group',
        widget  = forms.CheckboxSelectMultiple,
        initial = list(Orders.objects.get(id=instance.pk).order_items.all().values_list('test_id',flat=True).order_by('id')),
        )
            self.fields['test_selections'].required = False

    def clean_number(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.number
        else:
            return self.cleaned_data['number']
    class Meta:
        model = Orders
        fields = ('id','number','status','origin','priority','insurance','doctor','diagnosis','note')
        
class PaymentForm(forms.ModelForm):
    #type = forms.ModelChoiceField(queryset=OrderPayments.objects.all(), widget=Select2Widget,empty_label=None,required=False)
    class Meta:
        model = OrderPayments
        fields = ('type',)
