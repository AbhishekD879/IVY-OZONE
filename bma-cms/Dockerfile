FROM registry-coral.symphony-solutions.eu/baseimage:v2
MAINTAINER Gennadii Shvetsov <gennadii.shvetsov@symphony-solutions.eu>
ENV WORKDIR /home/bma

#Adding artifacts
ADD dist ${WORKDIR}/dist
ADD node_modules ${WORKDIR}/node_modules

COPY keystone.conf ${WORKDIR}/keystone.conf

RUN chown -R bma:bma ${WORKDIR}/dist

USER bma
WORKDIR ${WORKDIR}
CMD ["supervisord","-c", "/home/bma/keystone.conf"]
EXPOSE 3000
