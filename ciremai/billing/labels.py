from . import models
from django.utils.translation import ugettext_lazy as _
import serial,time
from utils import MiddlewareTask

class Label(object):
    labelprinter_id = 0
    order_id = 0
    
    def set_labelprinter_id(self,lp_id):
        self.labelprinter_id = lp_id
        return 
        
    def set_order_id(self,ord_id):
        self.order_id = ord_id
        return
    
    def print_label(self):
        order = models.Orders.objects.get(pk=self.order_id)
        samples = models.OrderTests.objects.filter(order = order).values('test__specimen__id','test__specimen__suffix_code').distinct()
        for sample in samples:
            models.OrderSamples.objects.get_or_create(order=order,specimen_id=sample['test__specimen__id'],sample_no=str(order.number+sample['test__specimen__suffix_code']))
            
            
        mw_task = MiddlewareTask()
        
        mw_task.set_order_id(self.order_id)
        mw_task.set_orderresult()
        
        #print sample
        labels = models.OrderSamples.objects.filter(order=order).values('sample_no','specimen__name')
        LF  = b'\x0A'

        port_com = models.LabelPrinters.objects.get(pk=self.labelprinter_id)
        
        try:
            label_com = serial.Serial(port= port_com.com_port,baudrate=9600,
                                            timeout=10, writeTimeout=10,stopbits=serial.STOPBITS_ONE,
                                            bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)
            for label in labels:
                #print label
                zpl_str = ''
                zpl_str = LF+'N'+LF
                zpl_str += 'A32,80,0,0,1,1,N,""'+LF
                zpl_str += 'A136,8,0,0,1,1,N,"'+order.number+'"'+LF
                zpl_str += 'A368,120,3,0,1,1,N,"'+label['specimen__name']+'"'+LF
                zpl_str += 'A16,32,0,0,1,1,N,"'+order.patient.name+'"'+LF
                zpl_str += 'A16,8,0,0,1,1,N,"Order Id :"'+LF
                zpl_str += 'A16,56,0,0,1,1,N,"RM :"'+LF
                zpl_str += 'A336,64,3,0,1,1,N,""'+LF # nomor urut
                zpl_str += 'A208,48,0,0,1,1,N,"'+order.patient.dob.strftime("%Y-%m-%d")+'"'+LF
                zpl_str += 'A72,48,0,0,1,1,N,"'+order.patient.patient_id+'"'+LF
                zpl_str += 'B32,80,0,1,2,4,136,B,"'+label['sample_no']+'"'+LF
                zpl_str += 'P1'+LF+LF
                
                label_com.write(zpl_str.encode())
                time.sleep(0.1)
        except Exception as e:
            return False,str(e)
        
        return True,_("Printer [%s] OK with serial port [%s]." % (port_com.name,port_com.com_port))
            
        