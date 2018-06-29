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
    
    def print_label_test(self):
        LF  = b'\x0A'
        try:
            label_com = serial.Serial(port= port_com.com_port,baudrate=9600,
                                            timeout=10, writeTimeout=10,stopbits=serial.STOPBITS_ONE,
                                            bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)
            zpl_str = ''
            zpl_str = '^XA^LH0,'
            zpl_str += '0^FO16,'
            zpl_str += '8^A^A0N,'
            zpl_str += '24,'
            zpl_str += '24^FWN^FDOrderNo^FS^FO104,'
            zpl_str += '8^A^A0N,'
            zpl_str += '24,'
            zpl_str += '24^FWN^FD180XXXXXXX^FS^FO16,'
            zpl_str += '56^A^A0N,'
            zpl_str += '24,'
            zpl_str += '24^FWN^FDNo.MR^FS^FO16,'
            zpl_str += '32^A^A0N,'
            zpl_str += '24,'
            zpl_str += '24^FWN^FDNAMA PASIEN^FS^FO88,'
            zpl_str += '56^A^A0N,'
            zpl_str += '24,'
            zpl_str += '24^FWN^FDXXXXXX^FS^FO248,'
            zpl_str += '56^A^A0N,'
            zpl_str += '24,'
            zpl_str += '24^FWN^FD01/01/1999^FS^FO32,'
            zpl_str += '80^A^A0N,'
            zpl_str += '0,'
            zpl_str += '0^FWN^FD^FS^FO368,'
            zpl_str += '120^A^A0N,'
            zpl_str += '27,'
            zpl_str += '27^FWB^FDURINE^FS^FO192,'
            zpl_str += '56^A^A0N,'
            zpl_str += '24,'
            zpl_str += '24^FWN^FDFemale^FS^FO32,'
            zpl_str += '80^BY2^BCN,'
            zpl_str += '136,'
            zpl_str += 'Y^FD180XXXXXXXU^FS^XZ,'
            zpl_str += '~HM'+LF
            
            label_com.write(zpl_str.encode())
            time.sleep(0.1)
        except Exception as e:
            return False,str(e)
        
        return True,_("Printer [%s] OK with serial port [%s]." % (port_com.name,port_com.com_port))

        
    
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
                
                zpl_str = ''
                zpl_str = '^XA^LH0,'
                zpl_str += '0^FO16,'
                zpl_str += '8^A^A0N,'
                zpl_str += '24,'
                zpl_str += '24^FWN^FDOrderNo^FS^FO104,'
                zpl_str += '8^A^A0N,'
                zpl_str += '24,'
                zpl_str += '24^FWN^FD'+order.number+'^FS^FO16,'
                zpl_str += '56^A^A0N,'
                zpl_str += '24,'
                zpl_str += '24^FWN^FDNo.MR^FS^FO16,'
                zpl_str += '32^A^A0N,'
                zpl_str += '24,'
                zpl_str += '24^FWN^FD'+order.patient.name+'^FS^FO88,'
                zpl_str += '56^A^A0N,'
                zpl_str += '24,'
                zpl_str += '24^FWN^FD'+order.patient.patient_id+'^FS^FO248,'
                zpl_str += '56^A^A0N,'
                zpl_str += '24,'
                zpl_str += '24^FWN^FD'+order.patient.dob.strftime("%Y-%m-%d")+'^FS^FO32,'
                zpl_str += '80^A^A0N,'
                zpl_str += '0,'
                zpl_str += '0^FWN^FD^FS^FO368,'
                zpl_str += '120^A^A0N,'
                zpl_str += '27,'
                zpl_str += '27^FWB^FD'+label['specimen__name']+'^FS^FO192,'
                zpl_str += '56^A^A0N,'
                zpl_str += '24,'
                zpl_str += '24^FWN^FD'+order.patient.gender.ext_code+'^FS^FO32,'
                zpl_str += '80^BY2^BCN,'
                zpl_str += '136,'
                zpl_str += 'Y^FD'+label['sample_no']+'^FS^XZ,'
                zpl_str += '~HM'+LF
                
                label_com.write(zpl_str.encode())
                time.sleep(0.3)
        except Exception as e:
            return False,str(e)
        
        return True,_("Printer [%s] OK with serial port [%s]." % (port_com.name,port_com.com_port))
            
        