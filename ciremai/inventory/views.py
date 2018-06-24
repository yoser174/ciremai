# -*- coding: utf-8 -*-

import csv,datetime
from datetime import date, timedelta
from django.shortcuts import render,HttpResponseRedirect
from django.db.models import Sum,F,Case,When,Value,CharField
from django.db.models.functions import Coalesce
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse_lazy
from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django_tables2 import SingleTableView, RequestConfig
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from . import models,forms
from .tables import SupplierTable,VendorTable,ProductTable,StockinTable,UsingProductTable,SelectStockinTable,ReturningProductTable,SelectUsingProductTable,StockTable
from extra_views.advanced import UpdateWithInlinesView,NamedFormsetsMixin, CreateWithInlinesView,InlineFormSet
from .custom.mixins import UpdateWithInlinesAndModifiedByMixin,CreateWithInlinesAndModifiedByMixin
from django.contrib.auth.decorators import permission_required
from avatar.forms import PrimaryAvatarForm,UploadAvatarForm 
from avatar.views import _get_avatars
from avatar.models import Avatar
from avatar.signals import avatar_updated
from avatar.utils import invalidate_cache
from django.contrib import messages
from inventory.filters import ProductFilter,StockinFilter,UsingProductFilter,ReturningProductFilter
from django_tables2.export.views import ExportMixin

from django.http import StreamingHttpResponse
from django.http import HttpResponse

def direct_to_template(request,template,extra_context=None, **kwargs):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('login')
    context=extra_context or {}
    context["params"]=kwargs
    for (key,value) in context.items():
        if callable(value):
            context[key]=value()
    return TemplateResponse(request, template, context)


# ######################
# ##   Helper Views   ##
# ######################

def login_user(request):
    logout(request)
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse_lazy('dashboard'), permanent=True)
        else:
            messages.error(request, _("Wrong username and/or password."))

    return render(request,'registration/login.html')

def show_dashboard(request):
    suppliercount = models.Supplier.objects.all().count()
    productcount = models.Product.objects.all().count()
    context = {'suppliercount': suppliercount,'productcount':productcount}
    return render(request,'dashboard.html',context)


def AvatarChange(request,extra_context=None,next_override=None,upload_form=UploadAvatarForm,primary_form=PrimaryAvatarForm,
                 *args,**kwargs):
    if extra_context is None:
        extra_context = {}
        
    avatar, avatars = _get_avatars(request.user)
    if avatar:
        kwargs = {'initial':{'choice':avatar.id}}
    else:
        kwargs = {}
    upload_avatar_form = upload_form(user=request.user, **kwargs)
    primary_avatar_form = primary_form(request.POST or None,
                                       user=request.user,
                                       avatars=avatars, **kwargs)
    
    if request.method == 'POST':
        updated = False
        if 'choice' in request.POST and primary_avatar_form.is_valid():
            avatar = Avatar.objects.get(id=primary_avatar_form.cleaned_data['choice'])
            avatar.primary = True
            avatar.save()
            updated = True
            invalidate_cache(request.user)
            messages.success(request, _("Successfully updated your avatar."))
        if updated:
            avatar_updated.send(sender=Avatar, user=request.user, avatar=avatar)
        return render(request,'auth/avatar_change.html')
    
    context = {
        'avatar':avatar,
        'avatars':avatars,
        'upload_avatar_form':upload_avatar_form,
        'primary_avatar_form':primary_avatar_form,
        'next':next_override
        }
    context.update(extra_context)
    template_name = 'auth/avatar_change.html'
    return render(request, template_name, context)
    
            
def AvatarAdd(request,extra_context=None,next_override=None,upload_form=UploadAvatarForm,*args,**kwargs):
    if extra_context is None:
        extra_context = {}
    avatar,avatars = _get_avatars(request.user)
    upload_avatar_form = upload_form(request.POST or None,
                                     request.FILES or None,
                                     user = request.user)
    if request.method == 'POST' and 'avatar' in request.FILES:
        if upload_avatar_form.is_valid():
            avatar = Avatar(user=request.user, primary=True)
            image_file = request.FILES['avatar']
            avatar.avatar.save(image_file.name,image_file)
            avatar.save()
            invalidate_cache(request.user)
            messages.success(request, _("Successfully uploaded a new avatar."))
            avatar_updated.send(sender=Avatar, user=request.user, avatar=avatar)
            return render(request,'auth/avatar_change.html')
    context = {
        'avatar': avatar,
        'avatars': avatars,
        'upload_avatar_form': upload_avatar_form,
        'next': next_override,
    }
    context.update(extra_context)
    template_name = 'auth/avatar_add.html'
    return render(request, template_name, context)    
            
            
            
# #################################
# ##   Inventory Function Views  ##
# #################################

def stockin_qrcode(request):
    if request.method == 'POST':  
        storage_pk = request.POST.get('storage','')  
        return redirect('select_stockin',storage_pk=storage_pk)
    else:
        tempate = 'inventory/stockin-qrcode.html'
        storage = models.Storage.objects.all()
        context = {'storage':storage}
        return render(request,tempate,context)   

def using_product_storage(request):
    if request.method == 'POST':  
        storage_pk = request.POST.get('storage','')  
        return redirect('select_stockin',storage_pk=storage_pk)
    else:
        tempate = 'select/select_storage.html'
        storage = models.Storage.objects.all()
        context = {'storage':storage}
        return render(request,tempate,context)   


def using_product_select_stockin(request,storage_pk):
    stockin = models.StockIn.objects.filter(storage=storage_pk)
    selectstockin = SelectStockinTable(stockin)
    selectstockin.paginate(page=request.GET.get('page', 1), per_page=10)
    tempate = 'select/select_stockin.html'
    context = {'storage_pk':storage_pk,'stockintable':selectstockin}
    return render(request,tempate,context)
     
def create_usingproduct_from_stockin(request, stockin_pk):
    stockin = models.StockIn.objects.get(pk=stockin_pk)
    usingproduct = stockin.create_usingproduct(request)
    return redirect('usingproduct_edit', pk=usingproduct.pk)


def returning_product_instrument(request):    
    if request.method == 'POST' and request.POST.get('instrument',''):  
        instrument_pk = request.POST.get('instrument','')
        return redirect('select_usingproduct',instrument_pk=instrument_pk)
    else:
        tempate = 'select/select_instrument.html'
        instrument = models.Instrument.objects.all()
        context = {'instrument':instrument}
        return render(request,tempate,context) 

def returning_product_select_using(request,instrument_pk):
    usingproduct = models.UsingProduct.objects.filter(used_at=instrument_pk)
    selectusingproduct = SelectUsingProductTable(usingproduct)
    selectusingproduct.paginate(page=request.GET.get('page', 1), per_page=10)
    tempate = 'select/select_using.html'
    context = {'instrument_pk':instrument_pk,'selectusingproduct':selectusingproduct}
    return render(request,tempate,context)       
        
def create_returnproduct_from_use(request, usingproduct_pk):
    usingproduct = models.UsingProduct.objects.get(pk=usingproduct_pk)
    returningproduct = usingproduct.create_returningproduct(request)
    return redirect('returningproduct_edit', pk=returningproduct.pk)

def view_available_stock(request):
    stock = models.StockIn.objects.values('product__number',
                                             'product__name',
                                             '_stockin_lot__number',
                                             '_stockin_lot__expired',
                                             'storage__name').annotate(
                                                 lot_status=Case(When(_stockin_lot__expired__lt=date.today(), 
                                                                  then=Value('Expired!')),
                                                             When(_stockin_lot__expired__gt=date.today(), 
                                                                  _stockin_lot__expired__lt=date.today() + timedelta(days=30), 
                                                                  then=Value('Expired < 1 Month')),
                                                             default=Value('ok'),
                                                             output_field=CharField()),
                                                 available_quantity=Sum('quantity',
                                                                        field='quantity-usingproduct__unit_used+usingproduct__returningproduct__unit_return')
                                                                       )
    stocktable = StockTable(stock)
    stocktable.paginate(page=request.GET.get('page', 1), per_page=10)
    return render(request,'inventory/stock_list.html',{'stocktable':stocktable})

def view_available_stock_csv(request):
    filename = 'stock_'+datetime.datetime.today().strftime('%Y-%m-%d')+'.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+filename+'"'

    writer = csv.writer(response)
    writer.writerow(['Lot Status','Lot Expired','Product Number','Storage','Lot Number','Product Name','Available Qty'])
    stock_data = models.StockIn.objects.values('product__number',
                                             'product__name',
                                             '_stockin_lot__number',
                                             '_stockin_lot__expired',
                                             'storage__name').annotate(
                                                 lot_status=Case(When(_stockin_lot__expired__lt=date.today(), 
                                                                  then=Value('Expired!')),
                                                             When(_stockin_lot__expired__gt=date.today(), 
                                                                  _stockin_lot__expired__lt=date.today() + timedelta(days=30), 
                                                                  then=Value('Expired < 1 Month')),
                                                             default=Value('ok'),
                                                             output_field=CharField()),
                                                 available_quantity=Sum('quantity',
                                                                        field='quantity-usingproduct__unit_used+usingproduct__returningproduct__unit_return')
                                                                       )
    for d_line in stock_data:
        writer.writerow([d_line['lot_status'],d_line['_stockin_lot__expired'],d_line['product__number'],d_line['storage__name'],d_line['_stockin_lot__number'], d_line['product__name'],d_line['available_quantity']])
    
    return response
    

# ###########################
# ##   Class Based Views   ##
# ###########################    
   
class UserExtensionInline(InlineFormSet):
    model = models.UserExtension
    extra = 1
    max_num = 1
    can_delete = False
    exclude = ()
    
class ProductUnitInline(InlineFormSet):
    model = models.Unit
    extra = 1
    max_num = 1
    can_delete = False
    exclude = ()   
    
class StockinLotInline(InlineFormSet):
    model = models.StockInLot
    extra = 1
    max_num = 1
    can_delete = False
    exclude = ()  


# ###################
# ##   Base Views  ##
# ###################

class UpdateUserProfile(LoginRequiredMixin,NamedFormsetsMixin,UpdateWithInlinesView):
    model = User
    #inlines = [UserExtensionInline, ]
    #inlines_names = ['userprofile_formset']
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('home')

class PaginatedTableView(SingleTableView):
    filter_class = None

    def __init__(self, **kwargs):
        super(PaginatedTableView, self).__init__(**kwargs)
        self.object_list = self.model.objects.all()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        config = RequestConfig(request)
        table = self.table_class(self.object_list)
        config.configure(table)
        table.paginate(page=request.GET.get('page', 1), per_page=self.table_pagination)
        context[self.context_table_name] = table
        return self.render_to_response(context)
    
class FilteredSingleTableView(SingleTableView):
    filter_class = None

    def get_table_data(self):
        data = super(FilteredSingleTableView, self).get_table_data()
        self.filter = self.filter_class(self.request.GET, queryset=data)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(FilteredSingleTableView, self).get_context_data(**kwargs)
        context['filter'] = self.filter
        return context

class ListSuppliers(LoginRequiredMixin, PermissionRequiredMixin, PaginatedTableView):
    model = models.Supplier
    permission_required = 'inventory.view_supplier'
    login_url = settings.LOGIN_URL
    fields = ['name', 'rep','rep_phone']
    table_class = SupplierTable
    table_data = models.Supplier.objects.all()
    context_table_name = 'suppliertable'
    table_pagination = 10
    
class ViewSupplier(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Supplier
    permission_required = 'iventory.view_supplier'
    login_url = settings.LOGIN_URL
    
class CreateSupplier(LoginRequiredMixin,PermissionRequiredMixin,
                     NamedFormsetsMixin,CreateWithInlinesAndModifiedByMixin):
    model = models.Supplier
    permission_required = 'inventory.add_supplier'
    login_url = settings.LOGIN_URL
    fields = ['name','rep','rep_phone']
    #inlines = [SupplierPostalAddressInline, SupplierPhoneAddressInline, SupplierEmailAddressInline]
    #inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('supplier_list')
    
class EditSupplier(LoginRequiredMixin, PermissionRequiredMixin,
                   NamedFormsetsMixin, UpdateWithInlinesAndModifiedByMixin):
    model = models.Supplier
    permission_required = 'inventory.change_supplier'
    login_url = settings.LOGIN_URL
    fields = ['name','rep','rep_phone']
    #inlines = [SupplierPostalAddressInline, SupplierPhoneAddressInline, SupplierEmailAddressInline]
    #inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('supplier_list')


class DeleteSupplier(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Supplier
    permission_required = 'inventory.delete_supplier'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('supplier_list')
    
    
class ListVendors(LoginRequiredMixin, PermissionRequiredMixin, PaginatedTableView):
    model = models.Vendor
    permission_required = 'inventory.view_vendor'
    login_url = settings.LOGIN_URL
    fields = ['name', 'rep','rep_phone']
    table_class = VendorTable
    table_data = models.Supplier.objects.all()
    context_table_name = 'vendortable'
    table_pagination = 10
    
class ViewVendor(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Vendor
    permission_required = 'iventory.view_vendor'
    login_url = settings.LOGIN_URL
    
class CreateVendor(LoginRequiredMixin,PermissionRequiredMixin,
                     NamedFormsetsMixin,CreateWithInlinesAndModifiedByMixin):
    model = models.Vendor
    permission_required = 'inventory.add_vendor'
    login_url = settings.LOGIN_URL
    fields = ['name','rep','rep_phone']
    #inlines = [SupplierPostalAddressInline, SupplierPhoneAddressInline, SupplierEmailAddressInline]
    #inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('vendor_list')
    
class EditVendor(LoginRequiredMixin, PermissionRequiredMixin,
                   NamedFormsetsMixin, UpdateWithInlinesAndModifiedByMixin):
    model = models.Vendor
    permission_required = 'inventory.change_vendor'
    login_url = settings.LOGIN_URL
    fields = ['name','rep','rep_phone']
    #inlines = [SupplierPostalAddressInline, SupplierPhoneAddressInline, SupplierEmailAddressInline]
    #inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('vendor_list')


class DeleteVendor(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Vendor
    permission_required = 'inventory.delete_vendor'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('vendor_list')


class ListProducts(LoginRequiredMixin, PermissionRequiredMixin, FilteredSingleTableView):
    model = models.Product
    permission_required = 'inventory.view_product'
    login_url = settings.LOGIN_URL
    table_class = ProductTable
    table_data = models.Product.objects.all()
    context_table_name = 'producttable'
    filter_class = ProductFilter
    table_pagination = 10

class CreateProduct(LoginRequiredMixin,PermissionRequiredMixin,NamedFormsetsMixin,CreateWithInlinesView):
    model = models.Product
    permission_required = 'inventory.add_product'
    login_url = settings.LOGIN_URL
    #inlines = [ProductUnitInline]
    #inlines_names = ['productunit_formset']
    success_url = reverse_lazy('product_list')
    form_class = forms.ProductForm
    
class ViewProduct(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Product
    permission_required = 'iventory.view_product'
    login_url = settings.LOGIN_URL
    
class EditProduct(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesAndModifiedByMixin):
    model = models.Product
    permission_required = 'iventory.change_product'
    login_url = settings.LOGIN_URL
    #inlines = [ProductUnitInline, ProductTaxInline]
    #inlines_names = ['productunit_formset', 'producttax_formset']
    success_url = reverse_lazy('product_list')
    form_class = forms.ProductForm


class DeleteProduct(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Product
    permission_required = 'iventory.delete_product'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('product_list')
    

class ListStockin(LoginRequiredMixin, PermissionRequiredMixin, FilteredSingleTableView):
    model = models.StockIn
    permission_required = 'inventory.view_stockin'
    login_url = settings.LOGIN_URL
    table_class = StockinTable
    table_data = models.StockIn.objects.all()
    filter_class = StockinFilter
    context_table_name = 'stockintable'
    table_pagination = 10

class CreateStockin(CreateView):
    model = models.StockIn
    permission_required = 'inventory.add_stockin'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('stockin_list')
    form_class = forms.StockinForm
    
    def form_valid(self, form):
        form.instance.lastmodifiedby = self.request.user
        return super(CreateStockin, self).form_valid(form)


class ViewStockin(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.StockIn
    permission_required = 'iventory.view_stockin'
    login_url = settings.LOGIN_URL
    
class EditStockin(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesAndModifiedByMixin):
    model = models.StockIn
    permission_required = 'iventory.change_stockin'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('stockin_list')
    form_class = forms.StockinForm


class DeleteStockin(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.StockIn
    permission_required = 'iventory.delete_stockin'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('stockin_list')


class EditStockinLot(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesAndModifiedByMixin):
    model = models.StockInLot
    permission_required = 'iventory.change_stockin'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('stockin_list')
    form_class = forms.StockinLotForm
    
class ListUsingProduct(LoginRequiredMixin, PermissionRequiredMixin, FilteredSingleTableView):
    model = models.UsingProduct
    permission_required = 'inventory.view_usingproduct'
    login_url = settings.LOGIN_URL
    table_class = UsingProductTable
    table_data = models.UsingProduct.objects.all()
    filter_class = UsingProductFilter
    context_table_name = 'usingproducttable'
    table_pagination = 10
    
class CreateUsingProduct(LoginRequiredMixin,PermissionRequiredMixin,NamedFormsetsMixin,CreateWithInlinesView):
    model = models.UsingProduct
    permission_required = 'inventory.add_usingproduct'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('usingproduct_list')
    form_class = forms.UsingProductForm
    
class UsingProductSelect(LoginRequiredMixin, PermissionRequiredMixin, PaginatedTableView):
    model = models.UsingProduct
    permission_required = 'inventory.view_usingproduct'
    login_url = settings.LOGIN_URL
    table_class = UsingProductTable
    table_data = models.UsingProduct.objects.all()
    context_table_name = 'usingproducttable'
    table_pagination = 10
    
class EditUsingProduct(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesAndModifiedByMixin):
    model = models.UsingProduct
    permission_required = 'iventory.change_using_product'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('usingproduct_list')
    form_class = forms.UsingProductForm
    
class DeleteUsingProduct(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.UsingProduct
    permission_required = 'iventory.delete_usingproduct'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('usingproduct_list')
    
class ListReturningProduct(LoginRequiredMixin, PermissionRequiredMixin, FilteredSingleTableView):
    model = models.ReturningProduct
    permission_required = 'inventory.view_returningproduct'
    login_url = settings.LOGIN_URL
    table_class = ReturningProductTable
    table_data = models.ReturningProduct.objects.all()
    filter_class = ReturningProductFilter
    context_table_name = 'returningproducttable'
    table_pagination = 10

class EditReturningProduct(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesAndModifiedByMixin):
    model = models.ReturningProduct
    permission_required = 'iventory.change_returning_product'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('returningproduct_list')
    form_class = forms.ReturningProductForm
    
class DeleteReturningProduct(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.ReturningProduct
    permission_required = 'iventory.delete_returningproduct'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('returningproduct_list')
    
class ListProductStock(ExportMixin,LoginRequiredMixin, PermissionRequiredMixin, PaginatedTableView):
    model = models.Product
    permission_required = 'inventory.view_product'
    login_url = settings.LOGIN_URL
    table_class = ProductTable
    #table_data = models.StockIn.objects.values('product__number','product__name','_stockin_lot__number','_stockin_lot__expired','storage__name').annotate(available_quantity=Sum('quantity',field='quantity-usingproduct__unit_used+usingproduct__returningproduct__unit_return'))
    a_month_ago = date.today() - timedelta(days=30)
    table_data=models.StockIn.objects.values('product__number',
                                             'product__name',
                                             '_stockin_lot__number',
                                             '_stockin_lot__expired',
                                             'storage__name').annotate(
                                                 lot_status=Case(When(_stockin_lot__expired__lt=date.today(), 
                                                                  then=Value('Expired!')),
                                                             When(_stockin_lot__expired__gt=date.today(), 
                                                                  _stockin_lot__expired__lt=date.today() + timedelta(days=30), 
                                                                  then=Value('Expired < 1 Month')),
                                                             default=Value('ok'),
                                                             output_field=CharField()),
                                                 available_quantity=Sum('quantity',
                                                                        field='quantity-usingproduct__unit_used+usingproduct__returningproduct__unit_return')
                                                                       )
    context_table_name = 'productstocktable'
    table_pagination = 10
    
