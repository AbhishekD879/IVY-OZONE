#!/usr/bin/env bash

ETC_HOSTS=/etc/hosts
ACC_SHARING_LOCAL_IP=0.0.0.0
ACC_SHARING_HOSTNAME=accounts-sharing-dev0.coralsports.dev.cloud.ladbrokescoral.com


function removehost() {
    if [ -n "$(grep ${ACC_SHARING_HOSTNAME} ${ETC_HOSTS})" ]
    then
        echo "${ACC_SHARING_HOSTNAME} Found in your ${ETC_HOSTS}, Removing now...";
        sudo sed -i".bak" "/${ACC_SHARING_HOSTNAME}/d" ${ETC_HOSTS}
    else
        echo "${ACC_SHARING_HOSTNAME} was not found in your ${ETC_HOSTS}";
    fi
}


function addhost() {

    HOSTS_LINE="$ACC_SHARING_LOCAL_IP\t${ACC_SHARING_HOSTNAME}"
    if [ -n "$(grep ${ACC_SHARING_HOSTNAME} /etc/hosts)" ]
        then
            echo "${ACC_SHARING_HOSTNAME} already exists : $(grep ${ACC_SHARING_HOSTNAME} ${ETC_HOSTS})"
        else
            echo "Adding ${ACC_SHARING_HOSTNAME} to your ${ETC_HOSTS}";
            sudo -- sh -c -e "echo '${HOSTS_LINE}' >> ${ETC_HOSTS}";

            if [ -n "$(grep ${ACC_SHARING_HOSTNAME} /etc/hosts)" ]
                then
                    echo "${ACC_SHARING_HOSTNAME} was added successfully => $(grep ${ACC_SHARING_HOSTNAME} ${ETC_HOSTS})";
                else
                    echo "Failed to Add ${ACC_SHARING_HOSTNAME}, try again";
            fi
    fi
}

$@