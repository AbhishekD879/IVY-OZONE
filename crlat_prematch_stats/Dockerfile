FROM python:2.7.12

#RUN apk -U add gcc openssl linux-headers python-dev py-configobj
RUN pip install web.py
RUN pip install pyOpenSSL
ADD prematch_stats /prematch_stats
EXPOSE 8080
WORKDIR /prematch_stats
CMD ["sh", "-c", "python stats.py"]