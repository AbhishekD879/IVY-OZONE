FROM nginx:alpine
RUN rm -rf /etc/nginx/conf.d/*
COPY resources/etc/nginx/conf.d/* /etc/nginx/conf.d/
COPY resources/etc/nginx/nginx.conf /etc/nginx/nginx.conf
COPY resources/etc/nginx/htpasswd /etc/nginx/htpasswd


