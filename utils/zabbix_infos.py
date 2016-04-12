#!/usr/local/sbin/python3.5

import requests
import shutil
import datetime
import re

from zabbix_api import ZabbixAPI

def get_host_id(host_name):
    zapi = ZabbixAPI(server='http://127.0.0.1/zabbix')
    zapi.login('svc_monitoria', 'vk98v#m$')
    host_response = zapi.host.get({'filter': {'host': str(host_name.rstrip())}})#[0]['hostid']
    host_id = host_response[0]['hostid']

    return host_id

def get_image_by_item_id(item_id):
    s = requests.Session()


    payload = {'form_refresh': 1,
               'name':'svc_monitoria',
               'password':'vk98v#m$',
               'autologin': 1,
               'enter': 'Sign in'}

    print('Fazendo o login...')
    login = s.post('http://zabbix-server01.dc.nova/zabbix/index.php', data=payload)
    login.headers['Set-Cookie']

    chart_url = ('http://zabbix-server01.dc.nova/zabbix/chart3.php?'
                 'period=3600&name=Grafico&width=350&height=200&graphtype=0'
                 '&legend=1&items[0][itemid]={item_id}&items[0][sortorder]=0'
                 '&items[0][drawtype]=5&items[0][color]=7092BE').format(item_id=item_id)

    print('Baixando a imagem...')
    chart_page = s.get(chart_url, stream=True)

    #print(chart_page.content)
    return chart_page.content

def get_item_type(host_id, item_id):
    s = requests.Session()


    payload = {'form_refresh': 1,
               'name':'svc_monitoria',
               'password':'vk98v#m$',
               'autologin': 1,
               'enter': 'Sign in'}

    login = s.post('http://zabbix-server01.dc.nova/zabbix/index.php', data=payload)

    url = 'http://zabbix-server01.dc.nova/zabbix/items.php?form=update&hostid={host_id}&itemid={item_id}'.format(host_id=host_id,
                                                                                                                 item_id=item_id)
    
    item_page = s.get(url)
    tipo_item = re.findall('name="value_type_name" value="(.*?)"', item_page.text)[0]

    if tipo_item == 'Numeric (float)' or tipo_item == 'Numeric (unsigned)':
        return 'number'
    elif tipo_item == 'Character':
        return 'string'
    else:
        return 'unknown'

if __name__ == '__main__':
    with open('imagem.png', 'wb') as imagem:
        shutil.copyfileobj(get_image_by_item_id(31711), imagem)
