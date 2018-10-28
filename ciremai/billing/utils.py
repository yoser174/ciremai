from django.conf import settings
from . import models


def is_float(str):
    try:
      fl = float(str)
      return True
    except ValueError:
      return False
  
def get_decimal(str_value):
    str_value = str(str_value).replace(".", "")
    str_value = str(str_value).replace(",", ".")
    return str_value



class MiddlewareTask(object):
    order_id = 0
    
    
    def set_orderresult(self):
        if self.is_active():
            from middleware.models import OrderResults,OrderExtended
            
            
            
            order = models.Orders.objects.get(pk=self.order_id)
            oreder_extended = OrderExtended.objects.get_or_create(order = order)
            self.order = order
            order_test = models.OrderTests.objects.filter(order=order)
            print order
            print order_test
            for ot in order_test:
                # check if have child
                ot_child0 = models.Tests.objects.filter(parent_id=ot.test_id)
                if ot_child0.count() > 0:
                    # have childs
                    for ot_0 in ot_child0:
                        # check again if have child
                        ot_child1 = models.Tests.objects.filter(parent_id=ot_0.id)
                        if ot_child1.count():
                            for ot_1 in ot_child1:
                                self.insert_order_result(self.order_id,ot_1.id)
                        else:
                            self.insert_order_result(self.order_id,ot_0.id)
                                
                                
                else:
                    # dont hav a child so insert it if not exist
                    self.insert_order_result(self.order_id,ot.test_id)
            
    def insert_order_result(self,order_id,test_id):
        from middleware.models import OrderResults
        test = models.Tests.objects.get(pk=test_id)
        sample = models.OrderSamples.objects.filter(order_id=order_id,specimen_id=test.specimen_id)
        e_ot_child0 = OrderResults.objects.filter(order_id=order_id,test_id=test_id)
        if not e_ot_child0.count():
            unit = self.get_test_unit(test_id)
            ref_range = self.get_ref_range(test_id)
            i_test = OrderResults(order_id=order_id,test_id=test_id,unit=unit,ref_range=ref_range,sample_id=sample[0].id)
            i_test.save()
            
    def get_test_unit(self,test_id):
        if self.is_active():
            from middleware.models import TestParameters
            unit = TestParameters.objects.filter(test_id=test_id)
            if unit:
                return unit[0].unit
            
            
    def setup_range(self,alfa_value=None,operator=None,operator_value=None,lower=None,upper=None):
        if alfa_value:
            return alfa_value
        else:
            # numeric range
            if operator:
                return  str(operator)+' '+str(operator_value)
            else:
                # range
                return  str(lower)+' - '+str(upper)

            
    def get_ref_range(self,test_id):
        order = models.Orders.objects.get(pk=self.order_id)
        self.order = order
        if self.is_active():
            from middleware.models import TestRefRanges
            refrange = TestRefRanges.objects.filter(test_id=test_id).values('any_age','gender','age_from_type','age_from','age_to','operator','operator_value','lower','upper','alfa_value','special_info','gender_id')
            if refrange.count()>0:
                for range in refrange:
                    # any age & any gender
                    if range['any_age']:
                        # check gender
                        if not range['gender']:
                            return self.setup_range(alfa_value=range['alfa_value'],
                                             operator=range['operator'],
                                             operator_value=range['operator_value'],
                                             lower=range['lower'],
                                             upper=range['upper'])
                                            
                        else:
                            # gender set
                            if range['gender'] == self.order.patient.gender_id:
                                return self.setup_range(alfa_value=range['alfa_value'],
                                             operator=range['operator'],
                                             operator_value=range['operator_value'],
                                             lower=range['lower'],
                                             upper=range['upper'])
                    else:
                        # date range
                        # Days
                        if range['age_from_type']=='D':
                            if int(range['age_from']) <= (self.order.order_date - self.order.patient.dob).days <= int(range['age_to']):
                                if (not range['gender']) or (range['gender'] == self.order.patient.gender_id) :
                                    return self.setup_range(alfa_value=range['alfa_value'],
                                             operator=range['operator'],
                                             operator_value=range['operator_value'],
                                             lower=range['lower'],
                                             upper=range['upper'])
                        # Months
                        if range['age_from_type']=='M':
                            if int(range['age_from']) <= (self.order.order_date - self.order.patient.dob).months <= int(range['age_to']):
                                if (not range['gender']) or (range['gender'] == self.order.patient.gender_id) :
                                    return self.setup_range(alfa_value=range['alfa_value'],
                                             operator=range['operator'],
                                             operator_value=range['operator_value'],
                                             lower=range['lower'],
                                             upper=range['upper'])
                        # Years
                        if range['age_from_type']=='Y':
                            if int(range['age_from']) <= (self.order.order_date - self.order.patient.dob).months <= int(range['age_to']):
                                if (not range['gender']) or (range['gender'] == self.order.patient.gender_id) :
                                    self.setup_range(alfa_value=range['alfa_value'],
                                             operator=range['operator'],
                                             operator_value=range['operator_value'],
                                             lower=range['lower'],
                                             upper=range['upper'])
                                    
                                
                    
            
    def set_order_id(self,ord_id):
        self.order_id = ord_id
             
        
        
    def is_active(self):
        if 'middleware' in settings.INSTALLED_APPS:
            return True
        else:
            return False
