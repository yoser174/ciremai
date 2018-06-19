# -*- coding: utf-8 -*-
###############################
# Host HL7
#
# auth: Yoserizal
# date: 19 June 2018
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
####

import logging.config
import yaml
import configparser
import glob
import hl7
import MySQLdb
import time
from datetime import datetime
import os

VERSION = '0.0.0.1'
DIR_IN = 'c:\\*.hl7'

MY_SERVER = 'localhost'
MY_USER = 'mwconn'
MY_PASS = 'connmw'
MY_DB = 'ciremai'


with open('host_hl7.yaml', 'rt') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

my_conn = MySQLdb.connect(host=MY_SERVER,
                  user=MY_USER,
                  passwd=MY_PASS,
                  db=MY_DB)

def my_select(sql):
    logging.info(sql)
    cursor = my_conn.cursor()
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except MySQLdb.Error as e:
        logging.error(e)
        
def my_insert(sql):
    logging.info(sql)
    cursor = my_conn.cursor()
    try:
        cursor.execute(sql)
        my_conn.commit()
        return cursor.lastrowid
    except MySQLdb.Error as e:
        logging.error(e)
        my_conn.rollback()

def my_update(sql):
    logging.info(sql)
    cursor = my_conn.cursor()
    try:
        cursor.execute(sql)
        my_conn.commit()
        return cursor.lastrowid
    except MySQLdb.Error as e:
        logging.error(e)
        my_conn.rollback()

def main():
    # read ini file
    config = configparser.ConfigParser()
    config.read('host_hl7.ini')
    DIR_IN = config.get('General','dir_in')
    MY_SERVER = config.get('General','my_server')

    logging.debug('starting host hl7 version: %s' % VERSION)
    logging.debug('DIR_IN %s' % DIR_IN)
    logging.debug('MY_SERVER: %s' % MY_SERVER)

    files = glob.glob(DIR_IN)
    for name in files:
        logging.debug('got file: %s' % name)
        line = open(name).read()
        h = hl7.parse(line)
        order_no = ''
        order_no = str(h.segment('ORC')[3]).strip()
        data = my_select(" SELECT id FROM billing_orders WHERE number = '%s' " % order_no )
        logging.info(data)
        if len(data)>0:
            order_id = data[0][0]
            for obx in h['OBX']:
                tes_code = obx[3][0][0] or ''
                tes_result = obx[5]or ''
                tes_unit = str(obx[6][0]).replace('^','') or ''
                tes_ref = str(obx[7]).replace('^','-') or ''
                tes_flag = ''
                
                ts = time.time()
                timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                #print tes_unit

                val_datetime = str(str(obx[14])[:4]+'-'+str(obx[14])[4:6]+'-'+str(obx[14])[6:8]+' '+str(obx[14])[8:10]+':'+str(obx[14])[10:12]+':'+str(obx[14])[12:14]) or timestamp
                
                logging.info(' Got test_code [%s], result [%s], ref [%s] , unit [%s], flag [%s] ' % (tes_code,tes_result,tes_ref,tes_unit,tes_flag))
                # select mapping test
                data_tes = my_select(" SELECT id FROM billing_tests WHERE ext_code ='%s'  "
                                     % (tes_code))
                if len(data_tes)>0:
                    logging.info(data_tes)
                    test_id = data_tes[0][0]
                    logging.info(' Got mapped test_id [%s] for test_code [%s] ' % (test_id,tes_code))
                    # check if order result created
                    d_order_result = my_select(" SELECT id FROM middleware_orderresults WHERE order_id = '%s' AND test_id = '%s' " % (order_id,test_id))
                    if len(d_order_result)>0:
                        order_res_id = d_order_result[0][0]
                    else:
                        logging.info('Create new row for insert value.')
                        order_res_id = my_insert(" INSERT INTO middleware_orderresults (order_id,test_id,is_header,lastmodification,validation_status,print_status) VALUES ('%s','%s','%s','%s','%s','%s') "
                                                 % (order_id,test_id,'0',timestamp,'1','0'))

                    # insert without flag ,techval_user,techval_date,medval_user,medval_date
                    #
                    logging.info(" insert result (alfa_result,order_id,test_id,lastmodification) values ('%s','%s','%s','%s') " % (tes_result,order_id,test_id,timestamp)) 
                    last_id = my_insert(" INSERT INTO middleware_results (alfa_result,order_id,test_id,lastmodification) values ('%s','%s','%s','%s') "
                                        % (tes_result,order_id,test_id,timestamp))

                    # update result to inserted value
                    logging.info('last inserted id [%s]' % last_id)
                    print tes_unit
                    up = my_update(" UPDATE middleware_orderresults SET result_id = '%s',ref_range = '%s', unit = '%s',patologi_mark = '%s' , techval_user = 'HOST', medval_user = 'HOST' , techval_date = '%s' , medval_date = '%s' , validation_status = '3' WHERE order_id = '%s' AND test_id = '%s' "
                                   % (last_id,tes_ref,tes_unit,tes_flag,val_datetime,val_datetime,order_id,test_id))
                    if up==0:
                        logging.info('update OK')
                    else:
                        logging.error('update fail.')


        # remove file
        logging.info('remove file: %s ' % name)
        os.remove(name)
                        
if __name__ == "__main__":
    main()

