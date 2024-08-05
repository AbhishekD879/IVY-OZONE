package com.ladbrokescoral.oxygen.cms.configuration;

import java.util.Map;
import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@ConfigurationProperties(prefix = "api")
@Data
@Component
public class ApiProperties {
  private Map<String, ApiConfiguration> buildyourbet;
  private Map<String, ApiConfiguration> bppMaintenance;

  @Data
  public static class ApiConfiguration {
    private String url;
    private String secret;
  }
}
