package com.ladbrokescoral.oxygen.questionengine.configuration;

import com.ladbrokescoral.oxygen.config.KafkaConsumerConfig;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;
import org.springframework.context.annotation.Profile;

@Profile("!INTEGRATION-TEST")
@Configuration
@Import(KafkaConsumerConfig.class)
@ComponentScan(basePackages = "com.ladbrokescoral.oxygen")
public class CmsPushConfiguration {}
