FROM node

ADD vis-football-widget-3d vis-football-widget-3d
WORKDIR vis-football-widget-3d
ADD start.sh /vis-football-widget-3d/start.sh
RUN sed "s/https:\/\/vis-stg2-coral.symphony-solutions.eu/http:\/\/$MY_IP:8120/g" \
    config/dev.json > config/dev.json.$$ && mv config/dev.json.$$ config/dev.json

RUN sed "s/https:\/\/vis-tst2-coral.symphony-solutions.eu/http:\/\/$MY_IP:8120/g" \
    config/tst.json > config/tst.json.$$ && mv config/tst.json.$$ config/tst.json

RUN sed "s/https:\/\/vis-stg2-coral.symphony-solutions.eu/http:\/\/$MY_IP:8120/g" \
    config/stg.json > config/stg.json.$$ && mv config/stg.json.$$ config/stg.json

RUN sed "s/https:\/\/vis-coral.symphony-solutions.eu/http:\/\/$MY_IP:8120/g" \
    config/prod.json > config/prod.json.$$ && mv config/prod.json.$$ config/prod.json

RUN sed "s/http:\/\/localhost:5000/http:\/\/$MY_IP:5000/g" \
    webpack.config.js > webpack.config.js.$$ && mv webpack.config.js.$$ webpack.config.js

RUN npm config set loglevel warn
RUN npm install

EXPOSE 5000
CMD ["./start.sh"]
