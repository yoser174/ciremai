# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,HttpResponseRedirect

from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from extra_views.advanced import UpdateWithInlinesView,NamedFormsetsMixin, CreateWithInlinesView,InlineFormSet,ModelFormMixin
from django_tables2 import SingleTableView, RequestConfig
from django.conf import settings
from datetime import datetime
from reportlab.pdfgen import canvas
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from avatar.forms import PrimaryAvatarForm,UploadAvatarForm 
from avatar.views import _get_avatars
from avatar.models import Avatar
from avatar.signals import avatar_updated
from avatar.utils import invalidate_cache
from utils import is_float

from . import models,tables,filters,forms
from billing.models import Orders,OrderTests,Tests,Parameters

import os
from pyreportjasper import JasperPy




# ######################
# ##   Helper Views   ##
# ######################

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(needs_autoescape=True)
def initial_letter_filter(text, autoescape=True):
    first, other = text[0], text[1:]
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<strong>%s</strong>%s' % (esc(first), esc(other))
    return mark_safe(result)



@login_required(login_url='login_middleware')
class UpdateUserProfileMW(LoginRequiredMixin,NamedFormsetsMixin,UpdateWithInlinesView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'auth/user_form_middleware.html'
    success_url = reverse_lazy('home_middleware')

def login_user(request):
    logout(request)
    next_url = request.GET.get('next','')
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next_url = request.POST.get('next','')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if next_url<>'':
                    return HttpResponseRedirect(next_url)
                else:
                    return redirect(reverse_lazy('dashboard_middleware'), permanent=True)
        else:
            messages.error(request, _("Wrong username and/or password."))
            
    context = {'next':next_url}
    return render(request,'registration/login_middleware.html',context)

@login_required(login_url='login_middleware')
def show_dashboard(request):
    #suppliercount = models.Supplier.objects.all().count()
    #productcount = models.Product.objects.all().count()
    #context = {'suppliercount': suppliercount,'productcount':productcount}
    context = {}
    return render(request,'dashboard_middleware.html',context)

@login_required(login_url='login_middleware')
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
        return render(request,'auth/avatar_change_middleware.html')
    
    context = {
        'avatar':avatar,
        'avatars':avatars,
        'upload_avatar_form':upload_avatar_form,
        'primary_avatar_form':primary_avatar_form,
        'next':next_override
        }
    context.update(extra_context)
    template_name = 'auth/avatar_change_middleware.html'
    return render(request, template_name, context)
    
@login_required(login_url='login_middleware')           
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
            return render(request,'auth/avatar_change_middleware.html')
    context = {
        'avatar': avatar,
        'avatars': avatars,
        'upload_avatar_form': upload_avatar_form,
        'next': next_override,
    }
    context.update(extra_context)
    template_name = 'auth/avatar_add_middleware.html'
    return render(request, template_name, context)    




@login_required(login_url='login_middleware')
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
    


#####################
# Middleware function
#####################
@login_required(login_url='login_middleware')
def home(request):
    template = 'index_middleware.html'
    org_lab_name = Parameters.objects.filter(name = 'ORG_LAB_NAME')
    org_lab_address = Parameters.objects.filter(name = 'ORG_LAB_ADDRESS')
    context = {'org_lab_name':org_lab_name,'org_lab_address':org_lab_address}
    return render(request,template,context) 

@login_required(login_url='login_middleware')
def show_workarea(request):   
    data = Orders.objects.all()
    filter = filters.OrderFilter(request.GET,queryset=data)
    ordertable = tables.OrderResultTable(filter.qs)
    ordertable.paginate(page=request.GET.get('page', 1), per_page=10)
    
    RequestConfig(request).configure(ordertable)
    
    tempate = 'middleware/workarea.html'
    context = {'ordertable':ordertable,'filter':filter}
    return render(request,tempate,context)

@login_required(login_url='login_middleware')
def order_results_history(request,pk):
    order = Orders.objects.get(pk=pk)
    data = models.HistoryOrders.objects.filter(order_id=pk)
    
    if request.GET.get('test'):
        print request.GET.get('test')
        data = data.filter(test=request.GET.get('test'))
        
    if request.GET.get('action_user'):
        print request.GET.get('action_user')
        data = data.filter(action_user__contains=request.GET.get('action_user'))
        
    if request.GET.get('action_code'):
        print request.GET.get('action_code')
        data = data.filter(action_code__contains=request.GET.get('action_code'))
        
    if request.GET.get('action_text'):
        print request.GET.get('action_text')
        data = data.filter(action_text__contains=request.GET.get('action_text'))
    
    filter = filters.OrderHistoryFilter(request.GET,queryset=data)
    
    orderhist = tables.OrderHistoryTable(data)
    orderhist.paginate(page=request.GET.get('page', 1), per_page=20)
    tempate = 'middleware/order_history.html'
    context = {'order':order,'orderhist':orderhist,'filter':filter}
    return render(request,tempate,context)

@login_required(login_url='login_middleware')
def order_results_validate(request,pk):
    if request.user.is_authenticated():
        order_res = models.OrderResults.objects.filter(order_id=pk,validation_status=1).update(validation_status=2,validation_user=str(request.user),validation_date=datetime.now())
    return redirect('order_results', pk=pk)

@login_required(login_url='login_middleware')
def order_results_techval(request,pk):
    if request.user.is_authenticated():
        # create history
        tech_val = models.OrderResults.objects.filter(order_id=pk,validation_status=1).values('test_id')
        for tes in tech_val:
            test_id = tes['test_id']
            test = Tests.objects.get(pk=test_id)
            act_txt = 'Test %s technical validated' % (test)
            his_order = models.HistoryOrders(order_id=pk,test=test,action_code='TECHVAL',action_user=str(request.user),action_date=datetime.now(),action_text=act_txt)
            his_order.save()
        
        # update
        order_res = models.OrderResults.objects.filter(order_id=pk,validation_status=1).update(validation_status=2,techval_user=str(request.user),techval_date=datetime.now())
    return redirect('order_results', pk=pk)

@login_required(login_url='login_middleware')
def order_results_medval(request,pk):
    if request.user.is_authenticated():
        # create history
        med_val = models.OrderResults.objects.filter(order_id=pk,validation_status=2).values('test_id')
        for tes in med_val:
            test_id = tes['test_id']
            test = Tests.objects.get(pk=test_id)
            act_txt = 'Test %s medical validated' % (test)
            his_order = models.HistoryOrders(order_id=pk,test=test,action_code='MEDVAL',action_user=str(request.user),action_date=datetime.now(),action_text=act_txt)
            his_order.save()
        order_res = models.OrderResults.objects.filter(order_id=pk,validation_status=2).update(validation_status=3,medval_user=str(request.user),medval_date=datetime.now())
    return redirect('order_results', pk=pk)

@login_required(login_url='login_middleware')
def order_results_repeat(request,pk):
    if request.user.is_authenticated():
        #test = Tests.objects.get(pk=)
        #result = models.Results(order=)
        order = Orders.objects.get(pk=pk)
        test_id =  request.GET.get('test_id')
        tes = Tests.objects.get(pk=test_id)
        result = models.Results(order=order,test=tes)
        result.save()
        order_result = models.OrderResults.objects.get(order=order,test=tes)
        order_result.validation_status=0
        order_result.result = result
        order_result.techval_user = None
        order_result.techval_date = None
        order_result.medval_user = None
        order_result.medval_date = None
        order_result.patologi_mark = None
        order_result.save()
        order_res = models.OrderResults.objects.filter(order_id=pk,validation_status=1).update(validation_status=3,medval_user=str(request.user),medval_date=datetime.now())
        
         # create history
        act_txt = 'Result %s repeated' % (tes)
        his_order = models.HistoryOrders(order=order,test=tes,action_code='REPEAT',action_user=str(request.user),action_date=datetime.now(),action_text=act_txt)
        his_order.save()
    return redirect('order_results', pk=pk)

@login_required(login_url='login_middleware')
def order_results_print(request,pk):
    order = Orders.objects.get(pk=pk)
    
    input_file_header = settings.RESULT_REPORT_FILE_HEADER
    input_file_main = settings.RESULT_REPORT_FILE_MAIN
    input_file = settings.RESULT_REPORT_FILE
    
    ts = datetime.today().strftime('%Y%m%d%H%M%S')
    parameters ={'ORDER_ID': pk}
    output = settings.MEDIA_ROOT+'\\report\\'+str(order.number)+'_'+ts
    con = settings.JASPER_CONN
    
    jasper = JasperPy()

    jasper.compile(input_file_header)
    jasper.compile(input_file_main)
    
    jasper.process(
                input_file,
                output_file=output,
                format_list=["pdf"],
                parameters=parameters,
                db_connection=con,
                locale='en_US',  
                resource= settings.RESULT_REPORT_DIR
            )

    base_url =  request.build_absolute_uri('/')[:-1].strip("/")
    url_pdf = base_url+'/media/report/'+str(order.number)+'_'+ts+'.pdf'
    
    # save report URL
    oe, _created = models.OrderExtended.objects.get_or_create(order_id=pk)

    oe.result_pdf_url = url_pdf
    oe.save()
    
    # set validation printed
    if request.user.is_authenticated():
        order_res = models.OrderResults.objects.filter(order_id=pk,validation_status=3).update(validation_status=4,print_user=str(request.user),print_date=datetime.now())
    
    

    template = 'middleware/result_pdf_preview.html'
    context = {'order':order,'url_pdf' : url_pdf}
    return render(request,template,context)

@login_required(login_url='login_middleware')
def order_result_report(request,pk):
    template = 'middleware/result_pdf_preview.html'
    context = {'order':order,'url_pdf' : url_pdf}
    return render(request,template,context)

@login_required(login_url='login_middleware')
def order_results(request,pk):
    order = Orders.objects.get(pk=pk)
    if request.method == 'POST': 
        for p_tes in request.POST:
            if p_tes.startswith('test_'):
                o_order = Orders.objects.get(pk=pk)
                o_test = Tests.objects.get(pk=p_tes.split('_')[1])
                # check current result
                if request.POST.get( p_tes, '')<>'':
                    # get current result
                    cr_res_a = ''
                    try:
                        cr_res = models.OrderResults.objects.get(order=o_order,test=o_test)
                        cr_res_a = cr_res.result.alfa_result
                    except:
                        pass
                    
                    if not cr_res_a == request.POST.get( p_tes, ''):
                        if request.user.is_authenticated():
                            alfa_res = request.POST.get( p_tes, '')
                            o_result = models.Results(order=o_order,test=o_test,alfa_result=alfa_res)
                            o_result.save()
                            
                            flag = None
                            
                            ord_res = models.OrderResults.objects.get(order=o_order,test=o_test)
                            
                            
                            if is_float(alfa_res) and ord_res.ref_range:
                                if str(ord_res.ref_range).find(' - ') > 0:
                                    # range
                                    range = str(ord_res.ref_range).split(' - ')
                                    if float(range[0])  <= float(alfa_res) <= float(range[1]):
                                        flag = 'N'
                                    elif float(alfa_res) >= float(range[1]):
                                        flag = 'H'
                                    else:
                                        flag = 'L'
                                elif '<' in str(ord_res.ref_range) or '>' in str(ord_res.ref_range):
                                    range = str(ord_res.ref_range).split(' ')
                                    if str(range[0]) == '>':
                                        if float(alfa_res) > float(range[1]):
                                            flag = 'N'
                                        else:
                                            flag = 'L'
                                    elif str(range[0]) == '<':
                                        if float(alfa_res) < float(range[1]):
                                            flag = 'N'
                                        else:
                                            flag = 'H'
                                    elif str(range[0]) == '>=':
                                        if float(alfa_res) >= float(range[1]):
                                            flag = 'N'
                                        else:
                                            flag = 'H'
                                    elif str(range[0]) == '<=':
                                        if float(alfa_res) <= float(range[1]):
                                            flag = 'N'
                                        else:
                                            flag = 'H'
                           
                            else:
                                flag = 'A'
                                
                            
                            ord_res.result = o_result
                            ord_res.patologi_mark = flag
                            ord_res.validation_status = 1
                            ord_res.save()

                            # create history
                            act_txt = 'Result %s set for analyt %s ' % (request.POST.get( p_tes, ''),o_test)
                            his_order = models.HistoryOrders(order=o_order,test=o_test,action_code='RESENTRY',action_user=str(request.user),action_date=datetime.now(),action_text=act_txt)
                            his_order.save()
    
    # Reference Range update from 

    orders = Orders.objects.get(pk=pk)
    ordertests = models.OrderResults.objects.filter(order = orders).values('test_id',
                                                                           'test__test_group__name',
                                                                           'test__name',
                                                                           'test__result_type',
                                                                           'result__alfa_result',
                                                                           'is_header',
                                                                           'unit',
                                                                           'ref_range',
                                                                           'patologi_mark',
                                                                           'validation_status',
                                                                           'result__instrument__name',
                                                                           'techval_user',
                                                                           'medval_user'
                                                                           ).order_by('test__test_group__sort','test__sort')
    # save report URL
    oe, _created = models.OrderExtended.objects.get_or_create(order_id=pk)
    tempate = 'middleware/order_results.html'
    context = {'order':order,'orders':orders,'ordertests':ordertests}
    return render(request,tempate,context)






# ###################
# ##   Base Views  ##
# ###################
"""
class ListReceivedSample(LoginRequiredMixin, PermissionRequiredMixin, FilteredSingleTableView):    
    model = models.ReceivedSamples
    permission_required = 'billing.view_orders'
    login_url = settings.LOGIN_URL_BILLING
    table_class = tables.ReceivedSamplesTable
    table_data = models.ReceivedSamples.objects.all()
    context_table_name = 'receivedsamplestable'
    filter_class = filters.ReceivedSamplesFilter
    table_pagination = 10
    
class ListResults(LoginRequiredMixin, PermissionRequiredMixin, FilteredSingleTableView):    
    model = models.Orders
    permission_required = 'billing.view_orders'
    login_url = settings.LOGIN_URL_BILLING
    table_class = tables.OrderResultTable
    table_data = models.Orders.objects.all()
    context_table_name = 'orderstable'
    filter_class = filters.OrderFilter
    table_pagination = 10
"""   

