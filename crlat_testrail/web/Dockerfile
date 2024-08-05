#FROM ubuntu:14.04
#
FROM php:5.6-apache
RUN apt-get update
RUN apt-get install -y --force-yes \
    unzip \
    cron \
    wget \
    gzip \
    tar \
    php5-mysql \
    php5-curl \
    php5-ldap
#    apache2 php5 \
#    php5-mysql \
#    php5-curl \
#    php5-ldap \
ADD 000-default.conf /etc/apache2/sites-available/000-default.conf
ADD start.sh /start.sh
RUN wget http://downloads3.ioncube.com/loader_downloads/ioncube_loaders_lin_x86-64.tar.gz
RUN tar -zxvf ioncube_loaders_lin_x86-64.tar.gz -C /usr/local/
ADD php.ini /usr/local/etc/php/php.ini
#ADD 001-testrail.conf /etc/apache2/sites-available/
COPY testrail/ /var/www/html/testrail/
RUN mkdir -p /var/www/html/testrail/logs/
RUN chown -R www-data:www-data /var/www/html/testrail/logs/
RUN mkdir -p /opt/testrail/attachments/
RUN mkdir -p /opt/testrail/reports/
RUN chown -R www-data:www-data /opt/testrail
RUN chown -R www-data:www-data /var/www
WORKDIR /root
RUN wget http://www.gurock.com/downloads/testrail/testrail-migrate-testlink-1.9.zip
RUN unzip testrail-migrate-testlink-1.9.zip
VOLUME /shared_folder
WORKDIR /shared_folder
#VOLUME /var/www/
CMD ["/start.sh"]