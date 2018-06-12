import django_tables2 as tables

from .custom.custom_columns import ModelDetailLinkColumn, IncludeColumn, CssFieldColumn, LabelIconColumn,ButtonColumn

from django.utils.translation import ugettext_lazy as _

from django.utils.html import format_html
from django.utils.safestring import mark_safe


from .models import ReceivedSamples,HistoryOrders
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

class pdfColumn(tables.Column):
    def render(self, value):
        return format_html('<a href="{}" target="_blank" class="btn btn-default" role="button"> \
        <span class="fa fa-file-pdf-o"></span></a>', value)

class progressColumn(tables.Column):
    def render(self, value):
        clr = 'danger'
        if str(value) == '25':
            clr = 'danger'
        if str(value) == '50':
            clr = 'warning'
        if str(value) == '75':
            clr = 'success'
        if str(value) == '100':
            clr = 'info'
        return format_html('<div class="progress progress-striped"> \
        <div class="progress-bar progress-bar-'+clr+'" role="progressbar" style="width: {}%;"> \
        &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;\
        </div></div>', value)

class OrderResultTable(tables.Table):
    progs = progressColumn(accessor="orderextended.get_progress",verbose_name='')
    pdf_url = pdfColumn(accessor="orderextended.result_pdf_url",verbose_name='')
    edit_order = IncludeColumn(
        'middleware/include/orders_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False,
        accessor="orderextended.result_pdf_url"
    )
    
    
    

    class Meta:
        model = Orders
        exclude = ('id')
        #sequence = ('number')
        fields = ('order_date','number','priority','origin','patient.patient_id','patient.name')
        order_by = ('-number',)


        
    

        
class OrderHistoryTable(tables.Table):
    #total_price = CssFieldColumn('record.get_total_price.total',verbose_name=_('Total Price'),attrs = {"td":{"align":"right"}})
    #edit_order = IncludeColumn(
    #    'middleware/include/orders_row_edit_toolbar.html',
    #    attrs={"th": {"width": "120px"}},
    #    verbose_name=" ",
    #    orderable=False
    #)
        
    
    class Meta:
        model = HistoryOrders
        exclude = ('id')
        #sequence = ('number')
        fields = ('action_user','action_date','action_code','test','action_text',)
        #fields = ('order_date','number','priority','origin','patient.patient_id','patient.name')
        order_by = ('-action_date',)
