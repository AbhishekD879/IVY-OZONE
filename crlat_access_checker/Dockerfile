FROM debian:jessie


RUN sed --in-place 's/httpredir.debian.org/mirror.sov.uk.goscomb.net/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y --fix-missing --no-install-recommends \
    python \
    python-dev \
    python-virtualenv \
    python-setuptools \
    python-pip \
    libxml2-dev \
    libxslt-dev \
    libz-dev \
    psmisc \
    git \
    bash \
    nano
ADD health_check /health_check
WORKDIR /health_check
RUN pip install -r requirements.txt

CMD ["/usr/bin/python", "do_all.py"]