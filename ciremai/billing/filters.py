import django_filters
from .models import TestGroups,Tests,Orders,Patients

class TestGroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = TestGroups
        fields = ['name']

class TestFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Tests
        fields = ['test_group','name']
        
class OrderFilter(django_filters.FilterSet):
    number = django_filters.CharFilter(lookup_expr='icontains')
    patient__patient_id = django_filters.CharFilter(lookup_expr='icontains')
    patient__name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Orders
        fields = ['number','patient__patient_id','patient__name']
        
class PatientFilter(django_filters.FilterSet):
    patient_id = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    address = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Patients
        fields = ['patient_id','name','address']

class JMFilter(django_filters.FilterSet):
    #start_date = django_filters.DateFilter(name='order_date',lookup_type=('gt'))
    #end_date = django_filters.DateFilter(name='order_date',lookup_type=('lt'))
    #date_range = django_filters.DateRangeFilter(name='order_date')
    class Meta:
        model = Orders
        fields = ['order_date']
