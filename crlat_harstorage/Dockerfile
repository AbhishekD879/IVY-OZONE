FROM ubuntu:latest
RUN apt-get update
RUN apt-get -y --fix-missing install mongodb lib32stdc++6 python python-cairo python-rsvg python-setuptools wget
RUN easy_install pylons webob pymongo==2.8
#RUN mkdir -p /data/db
WORKDIR /build
ADD harstorage /build
#RUN wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/harstorage/harstorage-1.0-py2.7.egg
#RUN wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/harstorage/pagespeed_bin

RUN python setup.py bdist_egg
RUN easy_install dist/harstorage*.egg
WORKDIR /harstorage
RUN rm -rf /build
ADD crlat_harstorage_docker/resources/production.ini /harstorage/production.ini
ADD crlat_harstorage_docker/resources/pagespeed_bin /harstorage/pagespeed_bin
#RUN paster setup-app production.ini
EXPOSE 5050
ADD crlat_harstorage_docker/start.sh /start.sh
CMD ["/start.sh"]

