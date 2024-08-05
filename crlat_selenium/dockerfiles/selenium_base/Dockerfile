
FROM python:3.6-stretch

ENV TERM=xterm

#RUN sed --in-place 's/httpredir.debian.org/mirror.sov.uk.goscomb.net/' /etc/apt/sources.list
#RUN sed --in-place 's/deb http\:\/\/security/# deb http\:\/\/security/' /etc/apt/sources.list

RUN mkdir -p /var/cache/apt/archives/partial
RUN touch /var/cache/apt/archives/lock
RUN apt-get clean --allow-unauthenticated && apt-get update --allow-unauthenticated && apt-get dist-upgrade -y --allow-unauthenticated && apt-get install -y --fix-missing gnupg --allow-unauthenticated
ADD ./resources/linux_signing_key.pub /tmp/linux_signing_key.pub
RUN apt-key add /tmp/linux_signing_key.pub
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get clean && apt-get update

RUN apt-get install -y --fix-missing --allow-unauthenticated --allow-downgrades \
    tigervnc-standalone-server \
    sudo \
    libxml2-dev \
    libxslt-dev \
    libz-dev \
    openssl \
    libssl-dev \
    libffi-dev \
    hicolor-icon-theme \
    xfonts-base \
    psmisc \
    git \
    libgl1-mesa-dri \
    rsync \
    ffmpeg \
    dbus-x11 \
    nano \
    google-chrome-stable \
    gcc \
    unzip \
    keychain \
    openjdk-8-jre-headless \
    procps \
    graphviz

RUN wget https://download.gocd.org/binaries/17.12.0-5626/deb/go-agent_17.12.0-5626_all.deb
RUN dpkg -i go-agent_17.12.0-5626_all.deb
RUN rm -f go-agent_17.12.0-5626_all.deb

RUN wget https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv ./chromedriver /usr/bin/chromedriver
RUN chmod +rx /usr/bin/chromedriver

RUN apt-get autoremove -y --allow-unauthenticated

EXPOSE 5900-5950
#EXPOSE 5557
ADD ./resources/var/go/.vnc /var/go/.vnc
ADD ./resources/var/go/.ssh /var/go/.ssh
ADD ./resources/var/go/.pip /var/go/.pip
ADD ./resources/var/go/.pypirc /var/go/.pypirc
ADD resources/etc/default/go-agent /etc/default/go-agent

#RUN chown -R go:go /var/go/
#ADD ./resources/usr/local/share/ca-certificates/web-root.crt /usr/local/share/ca-certificates/web-root.crt
ADD ./resources/usr/local/share/ca-certificates/crlat-web-root.pem /usr/local/share/ca-certificates/crlat-web-root.pem
RUN update-ca-certificates
ADD ./resources/etc/supervisor/conf.d/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD ./start.sh /start.sh
ADD ./resources/usr/bin/start_record_video.sh /usr/bin/start_record_video.sh
ADD ./resources/usr/bin/stop_record_video.sh /usr/bin/stop_record_video.sh
ADD ./resources/usr/bin/start_vnc.sh /usr/bin/start_vnc.sh
ADD ./resources/usr/bin/start_noVNC.sh /usr/bin/start_noVNC.sh
ADD ./resources/usr/bin/start_go.sh /usr/bin/start_go.sh
ADD ./resources/usr/bin/simulate_connection.sh /usr/bin/simulate_connection.sh
ADD ./resources/usr/bin/run_one_test.sh /usr/bin/run_one_test.sh

RUN chown -R go:go /var/go/
RUN chmod -R 700 /var/go/.ssh
RUN echo "go ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/95-cloud-init-users
RUN ln -s `which ffmpeg` /usr/bin/avconv
RUN echo "\nalias ll='ls -la'\n" >> /etc/bash.bashrc
USER go
RUN ssh-agent /bin/sh -c "ssh-add /var/go/.ssh/id_rsa"
RUN ssh-keygen -y -f ~/.ssh/id_rsa > ~/.ssh/id_rsa.pub
VOLUME /lib/modules
VOLUME /var/go/
VOLUME /var/log/go-agent/
VOLUME /usr/share/go-agent
VOLUME /var/log/
USER root
RUN touch /var/log/go-agent/go-agent.log
RUN chown -R go:go /var/log/go-agent
RUN chown -R go:go /usr/share/go-agent
VOLUME /stream/
RUN rm -rf /GOCD-GPG-KEY.asc

EXPOSE 6080-6090
RUN git clone https://github.com/kanaka/noVNC.git

RUN mv noVNC /var/noVNC
RUN sudo chown -R go:go /var/noVNC
RUN mkdir /mnt/reports && chmod 777 /mnt/reports
WORKDIR /var/go

CMD ["/start.sh"]