**1. To run docker locally:**

docker-compose build/up (it will create topic 'timeline')

**2. To post message to the topic:**

docker exec -it [kafka_container_name] /bin/bash

cd /opt/kafka/bin

./kafka-console-producer.sh --broker-list localhost:9092 --topic timeline
