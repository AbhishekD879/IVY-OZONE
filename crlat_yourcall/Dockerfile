FROM python:2.7.12

#RUN apk -U add gcc openssl linux-headers python-dev py-configobj
ADD crlat_yourcall /crlat_yourcall
COPY /crlat_yourcall/web-root.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates
RUN mkdir -p /root/.pip
RUN echo "nameserver 192.168.192.174" >> /etc/resolv.conf
RUN cat /etc/resolv.conf
COPY /crlat_yourcall/resources/pip.conf /root/.pip/pip.conf
WORKDIR /crlat_yourcall
EXPOSE 8080

CMD ["sh", "-c", "pip install web.py pyOpenSSL crlat_ob_client && python yourcall.py"]