FROM openjdk:8-jdk-alpine

LABEL maintainer="Oleh Perushko <oleg.perushko@ladbrokescoral.com>"
RUN mkdir /opt
ENV APPLICATION_DIR /opt/cashout
ENV KAFKA_CERTIFICATES ${APPLICATION_DIR}/ssl
ENV NEWRELIC_VERSION 3.45.0
ENV JAVA_TOOL_OPTIONS "-Dfile.encoding=UTF-8 -Dnewrelic.config.log_level=warn -Dnewrelic.config.log_file_name=STDOUT -Dspring.profiles.active=CRL-DEV1 -Dnewrelic.config.labels='application:cashout; environment:CRL-DEV1; Product:Oxygen'"

RUN mkdir ${APPLICATION_DIR} && \
    cd ${APPLICATION_DIR} && \
    wget https://oss.sonatype.org/content/repositories/releases/com/newrelic/agent/java/newrelic-java/${NEWRELIC_VERSION}/newrelic-java-${NEWRELIC_VERSION}.zip && \
    unzip newrelic-java-${NEWRELIC_VERSION}.zip -d . && \
    mv ${APPLICATION_DIR}/newrelic/newrelic.jar . && \
    mv ${APPLICATION_DIR}/newrelic/newrelic.yml .

COPY ./build/libs/*.jar ${APPLICATION_DIR}/application.jar

RUN mkdir ${KAFKA_CERTIFICATES}
COPY ./build/resources/main/ssl/ ${KAFKA_CERTIFICATES}

WORKDIR ${APPLICATION_DIR}

HEALTHCHECK --interval=1m --timeout=30s \
    CMD curl --fail http://localhost:8080/health || exit 1

ENTRYPOINT ["java", "-javaagent:./newrelic.jar","-jar", "application.jar"]