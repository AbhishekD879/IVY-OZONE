package com.coral.oxygen.middleware.common.configuration;

import java.time.Duration;
import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@ConfigurationProperties(prefix = "df")
@Data
@Component
public class DFConfigurationProperties {

  private Timeout timeout = new Timeout();
  private Logging logging = new Logging();
  private int maxIdleConnections;
  private Duration keepAliveDuration;

  @Data
  public class Timeout {

    private Duration read;
    private Duration connect;
  }

  @Data
  public class Logging {

    private String level;
  }
}
