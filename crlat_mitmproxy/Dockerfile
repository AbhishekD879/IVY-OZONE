FROM alpine


ENV LANG=en_US.UTF-8
ADD ./requirements.txt /tmp/requirements.txt

RUN apk add --update \
    python3 \
    python3-dev \
    py-pip \
    build-base \
    git \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-turbo-dev \
    libwebp-dev \
    openssl-dev \
    bash \
    nano \
    && ln -s /lib /lib64 \
    && pip3 install -r /tmp/requirements.txt \
    && rm -rf /var/cache/apk/* \
    && rm -rf ~/.cache/pip /tmp/pip_build_root

#ADD ca /root/.mitmproxy
# Location of the default mitmproxy CA files
# Expose ports
#   - 8080: Default mitmproxy port
#   - 8081: Default mitmweb port
EXPOSE 8080
EXPOSE 8081
VOLUME ["/root/.mitmproxy"]
#CMD ["sh"]
CMD ["/usr/bin/mitmweb", "--web-iface=0.0.0.0", "--no-browser"]