FROM ubuntu:14.04

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update \
    && apt-get install -y mysql-server \
    && rm -rf /var/lib/mysql
ADD my.cnf /etc/mysql/my.cnf
ADD start.sh /
ADD testrail_db.sql /
VOLUME /var/lib/mysql/

CMD [ "/start.sh" ]