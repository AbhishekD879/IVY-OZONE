#!/bin/bash
sudo mkdir -p /var/lib/go-agent/config
/bin/rm -f /var/lib/go-agent/config/autoregister.properties

MASTERHOST="${MASTERHOST:-unknown}"
AGENT_HOSTNAME=crlat_selenium_${DKR_ID}-on-$MASTERHOST
AGENT_RESOURCES=$AGENT_RESOURCES,$MASTERHOST
AGENT_ENVIRONMENTS=OxygenUI_test_docker_$MASTSER_AGENT_ENVIRONMENT
AGENT_KEY="${AGENT_KEY:-123456789abcdef}"
sudo touch /var/lib/go-agent/config/autoregister.properties
echo "agent.auto.register.key=$AGENT_KEY" | sudo tee /var/lib/go-agent/config/autoregister.properties
if [ -n "$AGENT_RESOURCES" ]; then echo "agent.auto.register.resources=$AGENT_RESOURCES" | sudo tee -a /var/lib/go-agent/config/autoregister.properties; fi
if [ -n "$AGENT_ENVIRONMENTS" ]; then echo "agent.auto.register.environments=$AGENT_ENVIRONMENTS" | sudo tee -a /var/lib/go-agent/config/autoregister.properties; fi
if [ -n "$AGENT_HOSTNAME" ]; then echo "agent.auto.register.hostname=$AGENT_HOSTNAME" | sudo tee -a /var/lib/go-agent/config/autoregister.properties; fi
touch /var/log/go-agent/go-agent-stderr.log
sudo chown -R go:go /var/lib/go-agent/config
/usr/share/go-agent/agent.sh go-agent service_mode
