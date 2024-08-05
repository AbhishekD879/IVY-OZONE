package com.ladbrokescoral.oxygen.trendingbets.configuration;

import java.time.Duration;
import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "app.client.http")
@Data
public class HttpClientProperties {

  private int connectTimeout;

  private boolean keepAlive;

  private int tcpKeepIdle;

  private int keepInterval;

  private int keepCount;

  private int readTimeout;

  private int maxConnections;

  private Duration maxIdleTime;

  private Duration maxLifeTime;

  private Duration pendingAcquireTimeout;

  private Duration evictInBackground;

  private int defaultClientMaxConnections;
}
