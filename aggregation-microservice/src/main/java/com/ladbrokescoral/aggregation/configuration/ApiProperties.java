package com.ladbrokescoral.aggregation.configuration;

import java.time.Duration;
import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "api")
@Data
public class ApiProperties {

  private Image image;
  private DataFeed df;

  @Component
  @ConfigurationProperties(prefix = "image")
  @Data
  public static class Image {

    private int numberOfRetries;
    private Duration readTimeout;
    private Duration writeTimeout;
    private Duration connectionTimeout;
    private String racingpost;
    private String teamtalk;
  }

  @Component
  @ConfigurationProperties(prefix = "df")
  @Data
  public static class DataFeed {

    private String endpoint;
    private Duration timeout;
  }
}
