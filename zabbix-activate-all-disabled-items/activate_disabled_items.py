#!/usr/bin/env python

from pyzabbix import ZabbixAPI
from pyzabbix import ZabbixAPIException
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-z', '--zabbix_url', dest='zabbix_host',
                  help='Zabbix Server host')
parser.add_option('-u', '--user',
                  dest='user',
                  help='Zabbix Server user')
parser.add_option('-p', '--password',
                  dest='password',
                  help='Zabbix Server password')
parser.add_option('-n', '--node',
                  dest='node',
                  help='Zabbix nodename')


(options, args) = parser.parse_args()
if options.zabbix_host is None:
    parser.error('Zabbix hostname not given')
elif options.user is None:
    parser.error('User not given')
elif options.password is None:
    parser.error('Password not given')


def connect_to_host(host, user, password):
    print "Connecting to " + host
    api = ZabbixAPI(host)
    api.login(user, password)
    print("Connected to Zabbix API Version %s" % api.api_version())
    return api


def get_hostid_by_name(api, node):
    print "Get host_id from group: \"" + str(node) + "\""
    params = {
        "filter": {"host": [node]}
    }

    response = api.do_request('host.get', params)
    result = response.get('result')[0].get('hostid')
    return result


def get_items_by_hostid(api, host_id):
    print "Get items from host: \"" + str(host_id) + "\""
    params = {
        "filter": {"hostid": [host_id]}
    }
    response = api.do_request('item.get', params)
    result = response.get('result')
    return result


def activate_item_by_hostid(api, item):
    print "Activate item: \"" + str(item.get('name')) + "\""
    params = {
        "itemid": item.get('itemid'),
        "status": 0
    }
    response = api.do_request('item.update', params)
    result = response.get('result')
    return result


def deactivate_item_by_hostid(api, item):
    print "Deactivate item: \"" + str(item.get('name')) + "\""
    params = {
        "itemid": item.get('itemid'),
        "status": 1
    }
    response = api.do_request('item.update', params)
    result = response.get('result')
    return result


zab_api = connect_to_host(options.zabbix_host, options.user, options.password)
host_id = get_hostid_by_name(zab_api, options.node)
items  = get_items_by_hostid(zab_api, host_id)

for item in items:
    if 'key_' in item.keys():
        if "webaccess" in item.get('key_'):
            deactivate_item_by_hostid(zab_api, item)
