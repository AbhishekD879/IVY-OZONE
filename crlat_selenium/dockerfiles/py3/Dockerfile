
FROM crlat_selenium_base

#RUN apt-get install -y --fix-missing --allow-downgrades \
#    python3 \
#    python3-dev \
#    python3-virtualenv \
#    python3-setuptools \
#    python3-xlib \
#    python3-pip
RUN pip install -U setuptools
RUN pip install \
        selenium\
        pytest \
        pytest-timeout \
        pytest-allure-adaptor \
        requests \
        psutil \
        Faker \
        pylint \
        pytest-profiling

#RUN ln -s `which python3` /usr/bin/python
#RUN ln -s `which pip3` /usr/bin/pip
USER go


