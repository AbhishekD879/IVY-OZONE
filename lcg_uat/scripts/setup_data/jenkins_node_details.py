import jenkins
import logging

label = 'dev-slave-crlat-ui-10'
node_info_list = [['Node_Name,  Available_Agents']]
offline_nodes = []
lads_total_nodes = 0
lads_total_executor = 0
coral_total_nodes = 0
coral_total_executor = 0
logger = logging.getLogger('voltron_logger')

server = jenkins.Jenkins('https://jenkins-vie.coral.co.uk/', username='mohd.siddiqui', password='6VysUxGNK8VcJXh4UF')
list_nodes = server.get_nodes()
for node in list_nodes:
    if label in node['name']:
        if not node['offline']:
            executor_size = len(list(server.get_node_info(node['name'], 0).get('executors')))
            if node['name'].startswith(label):
                coral_total_executor = coral_total_executor + executor_size
                coral_total_nodes = coral_total_nodes + 1
            else:
                lads_total_executor = lads_total_executor + executor_size
                lads_total_nodes = lads_total_nodes + 1
            node_info_list.append(list([node['name'], executor_size]))
        else:
            offline_nodes.append(node['name'])

if len(offline_nodes) > 0:
    print('############### OFFLINE Node details ###############')
    for item in offline_nodes:
        print(item)

print('\n\n############### CORAL Node details ###############')
print(f'\t#####Total Nodes available for CORAL {coral_total_nodes}')
print(f'\t#####Total agents available for CORAL {coral_total_executor}')

print('\n############### LADBROKES Node details ###############')
print(f'\t#####Total Nodes available for LADBROKES {lads_total_nodes}')
print(f'\t#####Total agents available for LADBROKES {lads_total_executor}\n')
for item in node_info_list:
    print(item)
