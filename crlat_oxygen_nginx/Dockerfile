FROM nginx:alpine
RUN apk update
RUN apk add openssl curl
RUN rm -rf /etc/nginx/conf.d/*
#COPY resources/etc/nginx/conf.d/* /etc/nginx/conf.d/
COPY resources/etc/nginx /etc/nginx
VOLUME /etc/nginx/conf.d/
VOLUME /var/www
VOLUME /var/log/
EXPOSE 80

