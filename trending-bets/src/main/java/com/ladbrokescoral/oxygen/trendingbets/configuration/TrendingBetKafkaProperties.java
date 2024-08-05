package com.ladbrokescoral.oxygen.trendingbets.configuration;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "tb.kafka")
@Data
public class TrendingBetKafkaProperties {

  private String zookeeperServer;

  private String groupId;

  private String sessionTimeout;

  private String syncTime;

  private String autoCommitInterval;

  private String autoOffsetReset;
}
