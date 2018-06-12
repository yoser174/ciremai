# -*- coding: utf-8 -*-
import os
from pyreportjasper import JasperPy

def processing():
    input_file = os.path.dirname(os.path.abspath(__file__)) + \
                 '/examples/ResultReport.jrxml'
    output = os.path.dirname(os.path.abspath(__file__)) + '/output/examples'
    jasper = JasperPy()
    jasper.process(
        input_file, output_file=output, format_list=["pdf", "rtf"])



processing()
