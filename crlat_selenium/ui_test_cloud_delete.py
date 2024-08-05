#!/usr/bin/env python
import json
import os
import socket
import requests
from requests.auth import HTTPBasicAuth
goserver_address = os.getenv('GO_SERVER_ADDRESS', 'http://goserver.crlat.net:8153')
user = os.environ.get('GO_USER', 'gobot')
password = os.environ.get('GO_PASSWD', 'Secret#1')
agents = json.loads(requests.get('%s/go/api/agents' % goserver_address,
                                 auth=HTTPBasicAuth(user, password),
                                 headers={'Accept': 'application/vnd.go.cd.v4+json'},
                                 ).content)

#
env_name = 'OxygenUI_test_docker_%s' % os.environ.get('GO_ENVIRONMENT_NAME', 'crlat_vpc')
resources = os.environ.get('AGENT_RESOURCES_CONFIG', 'node, voltron')

def match_agent(agent):
    if 'gocd-server' in agent['environments']:
        return False
    if env_name in agent['environments']:
        for resource in resources.split(', '):
            if resource not in agent['resources']:
                return False
        return True

print 'Going to delete hosts in "%s" with resources "%s"' % (env_name, resources)
print '***'
print agents
print '***'
for agent in agents['_embedded']['agents']:
    if match_agent(agent):
        print requests.patch('%s/go/api/agents/%s' % (goserver_address, agent['uuid']),
                          auth=HTTPBasicAuth(user, password),
                          headers={'Accept': 'application/vnd.go.cd.v4+json', 'Content-Type': 'application/json'},
                          data='{ "agent_config_state": "Disabled"}'
                          ).content
        print requests.delete('%s/go/api/agents/%s' % (goserver_address, agent['uuid']),
                          auth=HTTPBasicAuth(user, password),
                          headers={'Accept': 'application/vnd.go.cd.v4+json',  'Content-Type': 'application/json'},
                          ).content
