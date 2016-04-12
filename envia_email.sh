#!/usr/local/sbin/python3.5

import sys, os
import re
import datetime
from utils import email_sender, zabbix_infos

if __name__ == '__main__':
    try:
        destinatario = sys.argv[1]
        assunto = sys.argv[2]
        dados = sys.argv[3]
    
        if dados == 'debug':
            dados = """
trigger_name=TESTE Alta utilizacao de CPU no DYNATRACESERVER
trigger_status=PROBLEM
trigger_severity=High
item_id=30344
item_name=Utilizacao de CPU
item_value=5.975893
host_name=DYNATRACESERVER
event_id=16998
"""



        with open('/usr/local/share/zabbix/alertscripts/log/email.log', 'a') as arquivo:
            arquivo.write(str(datetime.datetime.now()) + ': ' + destinatario + ' - ' + assunto + '\n') 

        trigger_name = re.findall(r'.*trigger_name=(.*)', dados, re.MULTILINE)[0].rstrip()
        trigger_status = re.findall('.*trigger_status=(.*)', dados)[0].rstrip()
        trigger_severity = re.findall('trigger_severity=(.*)', dados)[0].rstrip()
        item_id = re.findall('item_id=(.*)', dados)[0].rstrip()
        item_name = re.findall('item_name=(.*)', dados)[0].rstrip()
        item_value = re.findall('item_value=(.*)', dados)[0].rstrip()
        host_name = re.findall('host_name=(.*)', dados)[0].rstrip()
        event_id = re.findall('event_id=(.*)', dados)[0].rstrip()
    
        cores = {'OK': {'Average': 'green', 'High': 'green', 'Warning': 'orange'},
                 'PROBLEM': {'Average': 'orange', 'High': 'red', 'Warning': 'orange', 'Informational': 'blue'}}

        with open('/usr/local/share/zabbix/alertscripts/templates/template_email.html', 'r') as email_template:
            corpo_raw = email_template.read() 
            #print(corpo_raw)
            corpo_raw = corpo_raw.replace('{HOST.NAME}', host_name)
            corpo_raw = corpo_raw.replace('{TRIGGER.NAME}', trigger_name)
            corpo_raw = corpo_raw.replace('{ITEM.NAME1}', item_name)
            corpo_raw = corpo_raw.replace('{ITEM.VALUE1}', item_value)
            corpo_raw = corpo_raw.replace('{ITEM.ID}', item_id)

            imagem_grafico = zabbix_infos.get_image_by_item_id(item_id)
            host_id = zabbix_infos.get_host_id(host_name)
            tipo_item = zabbix_infos.get_item_type(host_id, item_id)
            

            if tipo_item == 'number':
                email_sender.envia_email_imagem([destinatario], [], assunto, corpo_raw, imagem_grafico, cores[trigger_status][trigger_severity])
    
    except Exception as e:
        with open('/usr/local/share/zabbix/alertscripts/logs/error.log', 'a') as arquivo:
            print('Erro!', e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            arquivo.write(str(datetime.datetime.now()) + ': ' + str(e) + '\n')
            arquivo.write(str(datetime.datetime.now()) + ': ' + str(exc_type) + ' - ' +  str(fname) + '-' + str(exc_tb.tb_lineno))

