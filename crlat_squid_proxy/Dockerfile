FROM alpine:3.2


RUN apk update \
    && apk add squid \
    && apk add curl \
    && rm -rf /var/cache/apk/*

COPY squid.conf /etc/squid/squid.conf
COPY start-squid.sh /usr/local/bin/

ENTRYPOINT ["/usr/local/bin/start-squid.sh"]