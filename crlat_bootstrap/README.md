to run:
1) ansible-playbook <name_of_playbook>_create.yml
2) ./crlat _vpc/ec2.py --refresh-cache
3) ansible-playbook reconfigure_dnasmasq.yml
4) ansible-playbook <name_of_playbook>_config.yml