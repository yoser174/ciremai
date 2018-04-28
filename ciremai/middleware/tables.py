import django_tables2 as tables

from .custom.custom_columns import ModelDetailLinkColumn, IncludeColumn, CssFieldColumn, LabelIconColumn,ButtonColumn

from django.utils.translation import ugettext_lazy as _

from .models import ReceivedSamples
from billing.models import Orders


class ReceivedSamplesTable(tables.Table):
    edit_test_group = IncludeColumn(
        'includes/testgroups_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
    
    class Meta:
        model = ReceivedSamples
        exclude = ('id')
        #sequence = ('orders', 'tubes')
        order_by = ('sort',)
        
        
class OrderResultTable(tables.Table):
    #total_price = CssFieldColumn('record.get_total_price.total',verbose_name=_('Total Price'),attrs = {"td":{"align":"right"}})
    edit_order = IncludeColumn(
        'middleware/include/orders_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
        
    
    class Meta:
        model = Orders
        exclude = ('id')
        #sequence = ('number')
        fields = ('order_date','number','priority','origin','patient.patient_id','patient.name')
        order_by = ('-number',)
        
