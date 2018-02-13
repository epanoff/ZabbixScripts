#!/usr/bin/env python

from pyzabbix import ZabbixAPI
from pyzabbix import ZabbixAPIException
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
parser.add_option('-n', '--macros_name',
                  dest='macros_name',
                  help='')
parser.add_option('-m', '--macros_value',
                  dest='macros_value',
                  help='')

(options, args) = parser.parse_args()
if options.zabbix_host is None:
    parser.error('Zabbix hostname not given')
elif options.user is None:
    parser.error('User not given')
elif options.password is None:
    parser.error('Password not given')
elif options.group is None:
    parser.error('Group not given')


def connect_to_host(host, user, password):
    print "Connecting to " + host
    api = ZabbixAPI(host)
    api.login(user, password)
    print("Connected to Zabbix API Version %s" % api.api_version())
    return api


def get_group_by_name(api, group):
    print "Get group_id from group: \"" + str(group) + "\""
    params = {
        "filter": {"name": [group]}
    }

    response = api.do_request('hostgroup.get', params)
    result = response.get('result')[0].get('groupid')
    return result


def get_hosts_by_group(api, group_id):
    print "Get hosts_id from group: \"" + str(group_id) + "\""
    params = {
        'output': ['host'],
        'groupids': [group_id]
    }
    response = api.do_request('host.get', params)
    result = response.get('result')
    return result


def add_macros_to_host(api, host, host_id, macros_name, macros_value):
    macros_name_formatted = "{$" + macros_name + "}"
    print "Add Macros " + macros_name + " " + macros_value + " to host " + host
    params = {
        "hostid": host_id,
        "macro": macros_name_formatted,
        "value": macros_value
    }

    result = ""
    try:
        result = api.do_request('usermacro.create', params)
    except ZabbixAPIException:
        print "Already exists"

    return result

def delete_macros_from_host_by_value(api, host_id,  macros_value):
    params = {
         "hostids": host_id
    }
    response = api.do_request('usermacro.get', params)
    result = response.get('result')
    for macro in result:
        print macro
        if macro.get('value') == macros_value:
            hostmacroid = macro.get('hostmacroid')
            print str(hostmacroid)
            params =  [str(hostmacroid)]
            response = api.do_request('usermacro.delete', params)
    return response


zab_api = connect_to_host(options.zabbix_host, options.user, options.password)

print zab_api

group_id = get_group_by_name(zab_api, options.group)
print group_id
hosts = get_hosts_by_group(zab_api, group_id)

print hosts

d = {1: 'a', 2: 'b'}
for host in hosts:
   add_macros_to_host(zab_api, host.get('host'), host.get('hostid'), options.macros_name, options.macros_value)

