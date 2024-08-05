package com.ladbrokescoral.oxygen.questionengine.configuration.properties;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@Data
@ConfigurationProperties("site-server")
public class
SiteServerProperties {
  private String baseUrl;
  private String apiVersion;
  private String loggingLevel;
  private int connectionTimeout;
  private int readTimeout;
  private int retriesNumber;
}
