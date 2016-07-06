#!/usr/bin/env python

from zabbix.api import ZabbixAPI
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-z', '--zabbix_url', dest='zabbix_host',
                  help='Zabbix host')
parser.add_option('-u', '--user',
                  dest='user',
                  help='Zabbix user')
parser.add_option('-p', '--password',
                  dest='password',
                  help='')
parser.add_option('-g', '--group',
                  dest='group',
                  help='Zabbix hostgroup')
parser.add_option('-i', '--item',
                  dest='item',
                  help='Zabbix item name')
(options, args) = parser.parse_args()
if options.zabbix_host is None:
    parser.error('Zabbix hostname not given')
elif options.user is None:
    parser.error('User not given')
elif options.password is None:
    parser.error('Password not given')
elif options.group is None:
    parser.error('Group not given')
elif options.item is None:
    parser.error('Item not given')

colors = ["C80000", "00C800", "0000C8", "C800C8",
          "00C8C8",  "C8C800", "C8C8C8", "960096",
          "009696", "969600", "969696", "FF0000",
          "00FF00", "0000FF", "FF00FF", "00FFFF",
          "FFFF00", "000000", "790E1F", "87AC4D"]


def create_list(list):
    i = 0
    lst = []
    for pn in list:
        d = {}
        d['itemid']=pn
        d['color']=colors[i]
        i += 1
        lst.append(d)
    return lst

print "Connecting to " + options.zabbix_host

zapi = ZabbixAPI(url=options.zabbix_host, user=options.user, password=options.password)

print "Get items from item: \"" + options.item + "\" on group: \"" + options.group + "\""
result1 = zapi.do_request('item.get',
                          {
                              'filter': {'name': options.item},
                              'output': 'extend',
                              'group' : options.group
                          })

graph_color_json = create_list([itemid['itemid'] for itemid in result1['result']])

print "Creating graph \"" + options.item + "\" on group: \"" + options.group + "\""
params = {
                            'name': options.item,
                            'width': 900,
                            'height': 200,
                            'gitems': graph_color_json
                           }

zapi.do_request('graph.create', params)
print "Ok"
