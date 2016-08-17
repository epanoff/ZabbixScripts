# ZabbixScripts

Need Zabbix modules for Python :

pip install py-zabbix

##create_graph.py

Is is script for creating graph by item on different hosts in same hostgroup.

Usage
```
create_graph.py -z http://zabbix-hostname -u zabbix_username -p zabbix_password -g "Host Group" -i "Item"
```
or for create graphics for each item on Template
```
create_graph.py -z http://zabbix-hostname -u zabbix_username -p zabbix_password -g "Host Group" -t "Template name"
```
