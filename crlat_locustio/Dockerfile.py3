FROM python:3.6-jessie

RUN apt update &&\
    apt install -y ca-certificates gcc libxml2-dev libxslt-dev && \
    pip3 install locustio pyzmq lxml && \
    mkdir /locust

COPY resources/.pip/pip.conf /root/.pip/pip.conf
COPY resources/.pypirc /root/.pypirc
COPY resources/install_reqs.sh /usr/local/bin/install_reqs.sh

VOLUME /root/host.id
VOLUME /locust
WORKDIR /locust
EXPOSE 8089 5557 5558
ENTRYPOINT [ "/usr/local/bin/install_reqs.sh" ]
