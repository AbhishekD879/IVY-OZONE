#!/bin/bash
curl -i https://vault.datafabric.infra.aws.ladbrokescoral.com:8200/v1/kafka_pki_dev/ca/pem > caroot.cer
keytool -keystore oxygen.truststore.jks -alias CARoot -import -file ./caroot.cer -storepass nc2019Spring  -keypass nc2019Spring -noprompt
curl -H "X-Vault-Token: 700dae41-da4e-928e-33c0-e79213cdde8f" -X POST https://vault.datafabric.infra.aws.ladbrokescoral.com:8200/v1/kafka_pki_dev/issue/consumer_df -d '{"common_name":"oxygen.consumer.df.kafka-dev", "ttl":"87000h"}' | tee >(jq -r .data.certificate > consumer.cert) >(jq -r .data.issuing_ca > consumer_issuing_ca.pem) >(jq -r .data.private_key > consumer-key.pem)
openssl pkcs12 -export -in consumer.cert -inkey consumer-key.pem -out consumer.p12 -name oxygen -CAfile consumer_issuing_ca.pem -caname caRoot -password pass:nc2019Spring
keytool -importkeystore -deststorepass nc2019Spring -destkeypass nc2019Spring -destkeystore oxygen.keystore.jks -srckeystore consumer.p12 -srcstoretype PKCS12 -srcstorepass nc2019Spring -alias oxygen
keytool -keystore oxygen.keystore.jks -alias CARoot -import -file ./caroot.cer -storepass nc2019Spring  -keypass nc2019Spring -noprompt
