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
parser.add_option('-t', '--template',
                  dest='template',
                  help='Zabbix template name')

(options, args) = parser.parse_args()
if options.zabbix_host is None:
    parser.error('Zabbix hostname not given')
elif options.user is None:
    parser.error('User not given')
elif options.password is None:
    parser.error('Password not given')
elif options.group is None:
    parser.error('Group not given')
elif (options.item is None) and (options.template is None):
    parser.error('Item name  or template name  not given')

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
        d['itemid'] = pn
        d['color'] = colors[i]
        i += 1
        lst.append(d)
    return lst


def connect_to_host(host, user, password):
    print "Connecting to " + host
    api = ZabbixAPI(url=host, user=user, password=password)
    return api


def get_items_by_name(api, template):
    print "Get template_id from template: \"" + template + "\""
    result = api.do_request('item.get',
                              {
                                  'filter': {'name': item},
                                  'output': 'extend',
                                  'group': group
                              })
    return result


def get_id_by_template_name(api, template):
    print "Get items from template: \"" + template + "\""
    result = api.do_request('template.get',
                              {
                                  'filter': {'host': template},
                                  'output': 'extend'
                              })
    result = [templateid['templateid'] for templateid in result['result']]
    return result[0]


def get_items_by_name_on_group(api, item, group):
    print "Get items from item: \"" + item + "\" on group: \"" + group + "\""
    result = api.do_request('item.get',
                              {
                                  'filter': {'name': item},
                                  'output': 'extend',
                                  'group': group
                              })

    return result


def get_item_names_by_name_template(api, t_id):
    print "Get items from template id \"" + t_id + "\""
    result = api.do_request('item.get',
                              {
                                  'output': 'extend',
                                  'templateids': t_id
                              })
    return [item_name['name'] for item_name in result['result']]


def get_color_json(list_of_items):
    result_list = create_list([itemid['itemid'] for itemid in list_of_items['result']])
    return result_list


def create_graph(api, item, group, gitems_list):
    print "Creating graph \"" + item + "\" on group: \"" + group + "\""
    params = {
                                'name': item,
                                'width': 900,
                                'height': 200,
                                'gitems': gitems_list
                               }
    api.do_request('graph.create', params)
    print "Ok"


zab_api = connect_to_host(options.zabbix_host, options.user, options.password)
if options.template is None:
    list_items = get_items_by_name_on_group(zab_api, options.item, options.group)
    graph_color_list = get_color_json(list_items)
    create_graph(zab_api, options.item, options.group, graph_color_list)
else:
    template_id = get_id_by_template_name(zab_api, options.template)
    items_names = get_item_names_by_name_template(zab_api, template_id)
    for item_name in items_names:
            list_items = get_items_by_name_on_group(zab_api, item_name, options.group)
            graph_color_list = get_color_json(list_items)
            try:
                create_graph(zab_api, item_name, options.group, graph_color_list)
            except Exception as detail:
                print "Cannot create graph \"" + item_name + "\"\n", detail
print "All done"
