
FROM crlat_selenium_base

RUN apt-get install -y --fix-missing --allow-downgrades \
    python \
    python-dev \
    python-virtualenv \
    python-setuptools \
    python-xlib \
    python-pip

RUN pip install --upgrade \
        selenium==2.53.6 \
        pytest==2.9.0 \
        pytest-allure-adaptor \
        pytest-timeout \
        enum \
        requests \
        supervisor \
        browsermob-proxy \
        psutil \
        Faker \
        pylint \
        pytest-profiling
USER go