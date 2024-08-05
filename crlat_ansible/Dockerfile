FROM alpine:3.4


RUN echo "===> Installing sudo to emulate normal OS behavior..."  && \
    apk --update add sudo                                         && \
    \
    \
    echo "===> Adding Python runtime..."  && \
    apk --update add python py-pip openssl ca-certificates py-lxml && \
    apk --update add --virtual build-dependencies \
                python-dev libffi-dev openssl-dev build-base  && \
    pip install --upgrade pip cffi                            && \
    \
    \
    echo "===> Installing Ansible..."                                && \
    pip install ansible docker-py lxml boto boto3 jmespath                 && \
    \
    \
    echo "===> Installing Ansible roles..."                          && \
    ansible-galaxy install cmprescott.xml && \
    \
    \
    echo "===> Installing handy tools (not absolutely required)..."  && \
    apk --update add sshpass openssh-client rsync git docker  && \
    \
    \
    echo "===> Removing package list..."  && \
    apk del build-dependencies            && \
    rm -rf /var/cache/apk/*               && \
    \
    \
    echo "===> Adding hosts for convenience..."  && \
    mkdir -p /etc/ansible                        && \
    echo 'localhost   ansible_connection=local' > /etc/ansible/hosts
ENV AWS_ACCESS_KEY_ID=AKIAIMF5EOPDPTIUVQEQ
ENV AWS_SECRET_ACCESS_KEY=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
ADD root /root
ADD etc/ansible/ec2.ini /etc/ansible/ec2.ini
ADD etc/ansible/ec2.py /etc/ansible/ec2.py
RUN ssh-keyscan -H bitbucket.org >> ~/.ssh/known_hosts
RUN chmod -R 700 /root/.ssh
WORKDIR /root/ansible

# default command: display Ansible version
CMD [ "ansible-playbook", "--version" ]