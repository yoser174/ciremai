# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django_tables2 import SingleTableView, RequestConfig
from django.conf import settings
from datetime import datetime
from reportlab.pdfgen import canvas
from django.http import HttpResponse

from . import models,tables,filters,forms
from billing.models import Orders,OrderTests,Tests

import os
from pyreportjasper import JasperPy


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
    
    

def show_all_orders(request):
    data = Orders.objects.all()
    if request.GET.get('order_date'):
        d_range = request.GET.get('order_date')
        #04/01/2018 - 04/30/2018
        start_date = d_range[:10]
        end_date = d_range[13:23]
        
        data = data.filter(order_date__range=[start_date,end_date] )
    
    
    if request.GET.get('number'):
        #print request.GET.get('number')
        data = data.filter(number__contains=request.GET.get('number'))
    
    if request.GET.get('patient__patient_id'):
        #print request.GET.get('patient__patient_id')
        data = data.filter(patient__patient_id__contains=request.GET.get('patient__patient_id'))
        
    if request.GET.get('patient__name'):
        #print request.GET.get('patient__name')
        data = data.filter(patient__name__contains=request.GET.get('patient__name'))

    filter = filters.OrderFilter(request.GET,queryset=data)

    
    ordertable = tables.OrderResultTable(data)
    ordertable.paginate(page=request.GET.get('page', 1), per_page=10)
    
    RequestConfig(request).configure(ordertable)
    
    tempate = 'middleware/list_orders.html'
    context = {'ordertable':ordertable,'filter':filter}
    return render(request,tempate,context)

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

def order_results_validate(request,pk):
    if request.user.is_authenticated():
        order_res = models.OrderResults.objects.filter(order_id=pk,validation_status=1).update(validation_status=2,validation_user=str(request.user),validation_date=datetime.now())
    return redirect('order_results', pk=pk)

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

def order_results_print(request,pk):
    order = Orders.objects.get(pk=pk)
    input_file = settings.RESULT_REPORT_FILE
    ts = datetime.today().strftime('%Y%m%d%H%M%S')
    parameters ={'ORDER_ID': pk}
    output = settings.MEDIA_ROOT+'\\report\\'+str(order.number)+'_'+ts
    con = settings.JASPER_CONN
    jasper = JasperPy()
    jasper.process(
        input_file,
        output_file=output,
        format_list=["pdf"],
        parameters=parameters,
        db_connection=con,
        locale='en_US'
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
    
def order_result_report(request,pk):
    
    template = 'middleware/result_pdf_preview.html'
    context = {'order':order,'url_pdf' : url_pdf}
    return render(request,template,context)

def order_results_print2(request,pk):
    order = Orders.objects.get(pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="somefilename.pdf"'
    p = canvas.Canvas(response)
    p.setLineWidth(.3)
    p.setFont('Helvetica', 12)
    
    # judul
    p.drawString(230,780,'HASIL PEMERIKSAAN')
     
    # sisi kiri
    p.drawString(30,750,'Nama')
    p.drawString(120,750,": "+str(order.patient.name))
    p.drawString(30,735,'No. RM')
    p.drawString(120,735,": "+str(order.patient.patient_id))
    p.drawString(30,720,'Alamat')
    p.drawString(120,720,": "+str(order.patient.address))
    
    # sisi kanan
    p.drawString(350,750,"No Lab")
    p.drawString(440,750,": "+str(order.number))
    
    
    # Table header
    p.line(30,700,580,700)
    p.drawString(30,685,"Nama Pemeriksaan")
    p.drawString(200,685,"Hasil")
    p.drawString(340,685,"Nilai Rujukan")
    p.drawString(480,685,"Informasi")
    p.line(30,680,580,680)
    
    ordertests = models.OrderResults.objects.filter(order = order,validation_status__gte=2).values('test_id',
                                                                           'test__test_group__name',
                                                                           'test__name',
                                                                           'test__result_type',
                                                                           'result__alfa_result',
                                                                           'is_header',
                                                                           'unit',
                                                                           'result__ref_range',
                                                                           'result__mark',
                                                                           'validation_status',
                                                                           'validation_user').order_by('test__test_group__sort','test__sort')
    # detail
    row = 0
    for res in ordertests:
        row_pos = int(665 - (row*15)) 
        p.drawString(30,row_pos,str(res['test__name']))
        if res['result__mark']:
            p.drawString(180,row_pos,'*')
        p.drawString(210,row_pos,str(res['result__alfa_result']))
        p.drawString(280,row_pos,str(res['unit']))
        if res['result__ref_range']:
            p.drawString(350,row_pos,str(res['result__ref_range']))
        row += 1
    
    p.showPage()
    p.save()
    
    # set validation printed
    if request.user.is_authenticated():
        order_res = models.OrderResults.objects.filter(order_id=pk,validation_status=3).update(validation_status=4,print_user=str(request.user),print_date=datetime.now())
    
    return response

def order_results_print2(request,pk):
    order = Orders.objects.get(pk=pk)
    template = 'middleware/order_result_print.html'
    context = {'order':order}
    if request.user.is_authenticated():
        order_res = models.OrderResults.objects.filter(order_id=pk,validation_status=2).update(validation_status=3,print_user=str(request.user),print_date=datetime.now())
    return render(request,template,context)

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
                            o_result = models.Results(order=o_order,test=o_test,alfa_result=request.POST.get( p_tes, ''))
                            o_result.save()
                            # try delete existing result
                            try:
                                o_orderresult = models.OrderResults.objects.get(order=o_order,test=o_test)
                                o_orderresult.delete()
                            except models.OrderResults.DoesNotExist,e:
                                pass
                            # try get unit
                            s_unit = ''
                            try:
                                test_unit = models.TestParameters.objects.get(test=o_test)
                                s_unit = test_unit.unit
                            except models.TestParameters.DoesNotExist,e:
                                pass
                            o_orderresult = models.OrderResults.objects.get_or_create(order=o_order,test=o_test,result=o_result,validation_status=1,unit=s_unit)
                            
                            # create history
                            act_txt = 'Result %s set for analyt %s ' % (request.POST.get( p_tes, ''),o_test)
                            his_order = models.HistoryOrders(order=o_order,test=o_test,action_code='RESENTRY',action_user=str(request.user),action_date=datetime.now(),action_text=act_txt)
                            his_order.save()
    else:
        order_tests = OrderTests.objects.filter(order_id=pk)
        #print order_tests
        for ot in order_tests:
            # try get unit
            o_tes,c = models.OrderResults.objects.get_or_create(order_id=pk,test_id=ot.test_id)
            if not o_tes.result_id:
                o_tes_res,c = models.Results.objects.get_or_create(order_id=pk,test_id=ot.test_id)
                o_tes.result_id = o_tes_res.id
                o_tes.save()
                     
            s_unit = ''
            try:
                test_unit = models.TestParameters.objects.get(pk=ot.test_id)
                s_unit = test_unit.unit
            except models.TestParameters.DoesNotExist,e:
                pass
                
            o_tes = models.OrderResults.objects.get(order_id=pk,test_id=ot.test_id)
            o_tes.unit = s_unit
            o_tes.save()
            # try get child
            try:
                m_tes = Tests.objects.filter(parent_id=ot.test_id)
                if m_tes.count() > 0:
                    c_tes = models.OrderResults.objects.get(order_id=pk,test_id=ot.test_id)
                    c_tes.is_header=1
                    c_tes.save()
                    for child in  m_tes:
                        s_unit = ''
                        try:
                            test_unit = models.TestParameters.objects.get(pk=child.id)
                            s_unit = test_unit.unit
                        except models.TestParameters.DoesNotExist,e:
                            pass           
                        m_child,c = models.OrderResults.objects.get_or_create(order_id=pk,test_id=child.id)
                        if not o_tes.result_id:
                            m_child_res,c = models.Results.objects.get_or_create(order_id=pk,test_id=ot.test_id)
                            m_child.result_id = m_child_res.id
                            #m_child.unit = s_unit
                            #print m_child.unit
                            m_child.save()
                        try:
                            m_child_child = Tests.objects.filter(parent_id=child.id)
                            if m_child_child.count()>0:
                                c_child = models.OrderResults.objects.get(order_id=pk,test_id=child.id)
                                c_child.is_header=1
                                c_child.save()                    
                            for child_child in m_child_child:                    
                                m_child_child = models.OrderResults.objects.get_or_create(order_id=pk,test_id=child_child.id)
                                if not m_child_child:
                                    m_child_child_res,c = models.Results.objects.get_or_create(order_id=pk,test_id=ot.test_id)
                                    m_child_child.result_id = m_child_child_res.id
                                    m_child_child.save()
                        except Tests.DoesNotExist,e:
                            pass
            except Tests.DoesNotExist,e:
                pass
            
            
            #print o_tes
            
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
                                                                           'medval_user').order_by('test__test_group__sort','test__sort')
    # save report URL
    oe, _created = models.OrderExtended.objects.get_or_create(order_id=pk)
    tempate = 'middleware/order_results.html'
    context = {'order':order,'orders':orders,'ordertests':ordertests}
    return render(request,tempate,context)



#####################
# Middleware function
#####################

def orders(request):
    template = 'middleware/list_orders.html'
    #context = {'form':forms.PatientForm}
    context = {}
    return render(request,template,context)


# ###################
# ##   Base Views  ##
# ###################

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
    

