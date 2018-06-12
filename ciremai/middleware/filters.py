import django_filters


from .models import ReceivedSamples,HistoryOrders
from billing.models import Orders

class ReceivedSamplesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = ReceivedSamples
        fields = ['lastmodification','supergroup']
        
class OrderFilter(django_filters.FilterSet):
    #order_date = django_filters.DateFilter(name='order_date',lookup_type=('gt'),) 
    number = django_filters.CharFilter(lookup_expr='icontains')
    patient__patient_id = django_filters.CharFilter(lookup_expr='icontains')
    patient__name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Orders
        fields = ['order_date','number','patient__patient_id','patient__name']
        
        
class OrderHistoryFilter(django_filters.FilterSet):
    #number = django_filters.CharFilter(lookup_expr='icontains')
    #patient__patient_id = django_filters.CharFilter(lookup_expr='icontains')
    #patient__name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = HistoryOrders
        fields = ['test','action_user','action_code','action_text']