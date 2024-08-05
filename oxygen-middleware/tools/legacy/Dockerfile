FROM registry-coral.symphony-solutions.eu/alpine-java:8.45.14
ENV WORKDIR /opt/oxygen-middleware-docker

RUN mkdir ${WORKDIR}
COPY ./build/libs/*.jar ${WORKDIR}/oxygen-middleware.jar

WORKDIR ${WORKDIR}

ENTRYPOINT ["java", "-jar", "oxygen-middleware.jar"]
