#!/bin/bash
curl -i https://vault.datafabric.infra.aws.ladbrokescoral.com:8200/v1/kafka_pki_prod/ca/pem > caroot.cer
keytool -keystore oxygen.truststore.jks -alias CARoot -import -file ./caroot.cer -storepass coralAdminPass1  -keypass coralAdminPass1 -noprompt
curl -H "X-Vault-Token: 30d0d6df-a0c6-9ed3-80f2-298c6f1b3509" -X POST https://vault.datafabric.infra.aws.ladbrokescoral.com:8200/v1/kafka_pki_prod/issue/consumer_df -d '{"common_name":"oxygen.consumer.df.kafka-prod", "ttl":"35000h"}' | tee >(jq -r .data.certificate > consumer.cert) >(jq -r .data.issuing_ca > consumer_issuing_ca.pem) >(jq -r .data.private_key > consumer-key.pem)
openssl pkcs12 -export -in consumer.cert -inkey consumer-key.pem -out consumer.p12 -name oxygen -CAfile consumer_issuing_ca.pem -caname caRoot -password pass:coralAdminPass1
keytool -importkeystore -deststorepass coralAdminPass1 -destkeypass coralAdminPass1 -destkeystore oxygen.keystore.jks -srckeystore consumer.p12 -srcstoretype PKCS12 -srcstorepass coralAdminPass1 -alias oxygen
keytool -keystore oxygen.keystore.jks -alias CARoot -import -file ./caroot.cer -storepass coralAdminPass1  -keypass coralAdminPass1 -noprompt