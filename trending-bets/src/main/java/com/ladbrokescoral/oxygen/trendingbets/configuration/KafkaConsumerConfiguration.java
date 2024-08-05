package com.ladbrokescoral.oxygen.trendingbets.configuration;

import java.util.Properties;
import kafka.consumer.ConsumerConfig;
import kafka.javaapi.consumer.ConsumerConnector;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

@Configuration
@RequiredArgsConstructor
@Profile("!TEST")
public class KafkaConsumerConfiguration {

  private final TrendingBetKafkaProperties trendingBetKafkaProperties;

  @Bean
  public ConsumerConnector consumerConnector(ConsumerConfig consumerConfigs) {
    return kafka.consumer.Consumer.createJavaConsumerConnector(consumerConfigs);
  }

  @Bean
  public ConsumerConfig consumerConfigs() {

    Properties props = new Properties();
    props.put("zookeeper.connect", trendingBetKafkaProperties.getZookeeperServer());
    props.put("group.id", trendingBetKafkaProperties.getGroupId());
    props.put("zookeeper.session.timeout.ms", trendingBetKafkaProperties.getSessionTimeout());
    props.put("zookeeper.sync.time.ms", trendingBetKafkaProperties.getSyncTime());
    props.put("auto.commit.interval.ms", trendingBetKafkaProperties.getAutoCommitInterval());
    props.put("auto.offset.reset", trendingBetKafkaProperties.getAutoOffsetReset());

    return new ConsumerConfig(props);
  }
}
