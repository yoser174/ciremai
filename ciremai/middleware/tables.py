import django_tables2 as tables

from .custom.custom_columns import ModelDetailLinkColumn, IncludeColumn, CssFieldColumn, LabelIconColumn,ButtonColumn

from django.utils.translation import ugettext_lazy as _

from .models import ReceivedSamples


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