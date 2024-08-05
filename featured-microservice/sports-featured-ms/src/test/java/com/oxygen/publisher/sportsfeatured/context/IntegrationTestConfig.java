package com.oxygen.publisher.sportsfeatured.context;

import com.oxygen.publisher.configuration.SocketIOConnectorConfiguration;
import com.oxygen.publisher.configuration.SocketIOServerConfiguration;
import com.oxygen.publisher.service.KafkaTopic;
import com.oxygen.publisher.sportsfeatured.configuration.*;
import com.oxygen.publisher.sportsfeatured.service.SportIdFilter;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.kafka.KafkaAutoConfiguration;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

@Configuration
@EnableAutoConfiguration(exclude = {KafkaAutoConfiguration.class})
@Import({
  FeaturedApiProvider.class,
  WorkersConfiguration.class,
  FeaturedKafkaRecordConsumer.class,
  FeaturedServiceConfiguration.class,
  SocketIOServerConfiguration.class,
  SocketIOServerConfigurationOverrides.class,
  SocketIOConnectorConfiguration.class,
  ServiceRegistryConfiguration.class,
  SportIdFilter.class,
  KafkaTopic.class
})
public class IntegrationTestConfig {}
