import django_tables2 as tables

from .models import Supplier, Product, StockIn, ReturningProduct, UsingProduct
from .custom.custom_columns import ModelDetailLinkColumn, IncludeColumn, CssFieldColumn, LabelIconColumn,ButtonColumn

from django.utils.translation import ugettext_lazy as _

class SupplierTable(tables.Table):
    name = ModelDetailLinkColumn(accessor='name')
    edit_supplier = IncludeColumn(
        'includes/supplier_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
    
    class Meta:
        model = Supplier
        exclude = ('id')
        sequence = ('name', 'rep')
        order_by = ('name',)

class VendorTable(tables.Table):
    name = ModelDetailLinkColumn(accessor='name')
    edit_vendor = IncludeColumn(
        'includes/vendor_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
    
    class Meta:
        model = Supplier
        exclude = ('id')
        sequence = ('name', 'rep')
        order_by = ('name',)
        
class ProductTable(tables.Table):
    base_unit = CssFieldColumn('record.base_unit.name')
    description = 'record.name'
    edit_product = IncludeColumn(
        'includes/product_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
    class Meta:
        model = Product
        exclude = ('id',  'dateofcreation', 'lastmodification', 'lastmodifiedby', 'vendor', 'temperature_condition', 'lead_time')
        sequence = ('number', 'name','lot_controlled', 'supplier')
        order_by = ('id',)
        
class StockinTable(tables.Table):
    #base_unit = CssFieldColumn('record.product.base_unit.name',verbose_name=_('Unit'),orderable=False)
    description = 'record.name'
    product = tables.TemplateColumn('<a href="{{ record.product.get_absolute_url }}">{{record.product}}</a>')
    lastmodifiedby = CssFieldColumn('record.lastmodifiedby',verbose_name=_('Created by'))
    
    edit_lot = ButtonColumn(gl_icon="hourglass-end",
                            extra_class="btn-info",
                            condition='record.product.lot_controlled and not record.stockin_lot.expired ',
                            onclick = "location.href='{{ record.stockin_lot.get_absolute_url }}'",
                            verbose_name=_('Lot'),orderable=False)
    
    edit_product = IncludeColumn(
        'includes/stockin_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
    class Meta:
        model = StockIn
        exclude = ('id', 'lastmodification','unit')
        sequence = ('date_in','storage','product','quantity', 'lastmodifiedby')
        order_by = ('id',)
    
class UsingProductTable(tables.Table):
    description = 'record.name'
    product = CssFieldColumn('record.stock_in.product',verbose_name=_('Product'))
    lot_no = CssFieldColumn('record.stock_in.stockin_lot.number',verbose_name=_('Lot No.'))
    lot_expired = CssFieldColumn('record.stock_in.stockin_lot.expired',verbose_name=_('Expired'))
    used_at = CssFieldColumn('record.used_at',verbose_name=_('Used at'))
    unit_used = CssFieldColumn('record.unit_used',verbose_name=_('Qty'))
    unit = CssFieldColumn('record.stock_in.product.base_unit.name',orderable=False)
    lastmodifiedby = CssFieldColumn('record.lastmodifiedby',verbose_name=_('Created by'))
    
    edit_product = IncludeColumn(
        'includes/usingproduct_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
    class Meta:
        model = UsingProduct
        exclude = ('id', 'lastmodification','supplier','storage','quantity')
        sequence = ('date_use','product','lot_no','lot_expired','used_at','unit_used','unit', 'lastmodifiedby')
        order_by = ('id',)
        
class SelectStockinTable(tables.Table):
    unit = CssFieldColumn('record.product.base_unit.name',orderable=False)
    description = 'record.name'
    product = LabelIconColumn(verbose_name=_('Product'))
    lot_no = CssFieldColumn('record.stockin_lot',verbose_name=_('Lot'))
    lot_expired = CssFieldColumn('record.stockin_lot.expired',verbose_name=_('Expired'))
    
    use_product = ButtonColumn(gl_icon="external-link",
                            extra_class="btn-info",
                            condition = '1',
                            onclick = "location.href='{% url 'stockin_create_usingproduct' record.pk %}'",
                            verbose_name=_(''),orderable=False)
    
    class Meta:
        model = StockIn
        exclude = ('id', 'lastmodification','storage','supplier','dateofcreation', 'lastmodifiedby')
        sequence = ('product','lot_no','lot_expired','quantity','unit')
        order_by = ('id',)
        
class ReturningProductTable(tables.Table):
    description = 'record.name'
    
    product = CssFieldColumn('record.using_product.stock_in.product',verbose_name=_('Product'))
    lot_no = CssFieldColumn('record.using_product.stock_in.stockin_lot.number',verbose_name=_('Lot No.'))
    lot_expired = CssFieldColumn('record.using_product.stock_in.stockin_lot.expired',verbose_name=_('Expired'))
    used_at = CssFieldColumn('record.using_product.used_at',verbose_name=_('Return from'))
    unit = CssFieldColumn('record.using_product.stock_in.product.base_unit.name',orderable=False)
    lastmodifiedby = CssFieldColumn('record.lastmodifiedby',verbose_name=_('Created by'))
    unit_used = CssFieldColumn('record.using_product.unit_used',verbose_name=_('Unit used'))
    
    edit_product = IncludeColumn(
        'includes/returningproduct_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
    class Meta:
        model = ReturningProduct
        exclude = ('id', 'lastmodification','using_product',)
        sequence = ('date_return','product','lot_no','lot_expired','used_at','unit', 'lastmodifiedby','unit_used')
        order_by = ('id',)

class SelectUsingProductTable(tables.Table):
    product = CssFieldColumn('record.stock_in.product',orderable=False,verbose_name=_('Product'))
    unit = CssFieldColumn('record.stock_in.product.base_unit.name',orderable=False)
    description = 'record.name'
    lot_no = CssFieldColumn('record.stock_in.stockin_lot.number',verbose_name=_('Lot'))
    lot_expired = CssFieldColumn('record.stock_in.stockin_lot.expired',verbose_name=_('Expired'))
    
    return_product = ButtonColumn(gl_icon="external-link",
                            extra_class="btn-info",
                            condition = '1',
                            onclick = "location.href='{% url 'using_create_return' record.pk %}'",
                            verbose_name=_(''),orderable=False)
    
    class Meta:
        model = UsingProduct
        exclude = ('id', 'stock_in','lastmodification','storage','supplier','dateofcreation', 'lastmodifiedby')
        sequence = ('product','lot_no','lot_expired','unit')
        order_by = ('id',)
        
class StockTable(tables.Table):
    #unit = CssFieldColumn('record.base_unit.name')
    description = 'record.name'
    #stockin_lot__number = CssFieldColumn('record.stockin_lot__number',verbose_name=_('Status'))
    storage__name = CssFieldColumn('record.storage__name',verbose_name=_('Storage'))
    product__number = CssFieldColumn('record.product__number',verbose_name=_('Product No.'))
    product__name = CssFieldColumn('record.product__name',verbose_name=_('Product Name'))
    #product__name = CssFieldColumn('record.stockin_lot.expired',verbose_name=_('Lot'))
    #available_quantity = CssFieldColumn('record.available_quantity',verbose_name=_('Available Qty'),attrs={'td':{'align':'center'}})
    
    class Meta:
        model = StockIn
        fields = ('lot_status','storage__name','product__number','product__name','_stockin_lot__number','_stockin_lot__expired','available_quantity')
        attrs = {
            'th':{
                'id':'available_quantity'
        }
            }
        #exclude = ('id', 'base_unit', 'dateofcreation', 'lastmodification', 'lastmodifiedby')
        #sequence = ('product')
        order_by = ('id',)