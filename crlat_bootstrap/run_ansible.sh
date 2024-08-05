#!/usr/bin/env bash
cmd_to_run=$@
docker run \
	-it --rm \
	--name=ansible-master \
	-v $PWD:/root/ansible \
	-w /root/ansible \
	-v /var/run/docker.sock:/var/run/docker.sock \
    -v $HOME/.ssh/bootstraper:/root/.ssh \
    -e AWS_ACCESS_KEY_ID=xxxxx \
    -e AWS_SECRET_ACCESS_KEY=xxxx \
	crlat_ansible sh
	#-c "$cmd_to_run" #sh -c "ansible-playbook -i 'localhost,' -vvv --connection=local StatCenter/start_middleware_docker.yml"
