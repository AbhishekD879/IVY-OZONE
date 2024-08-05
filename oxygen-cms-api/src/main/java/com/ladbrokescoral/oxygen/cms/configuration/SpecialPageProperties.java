package com.ladbrokescoral.oxygen.cms.configuration;

import java.util.Map;
import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@ConfigurationProperties(prefix = "specialpages")
@Data
@Component
public class SpecialPageProperties {
  private Map<String, SpecialPageProperties.ApiConfiguration> specialpageConfig;

  @Data
  public static class ApiConfiguration {
    private String url;
    private String secret;
  }
}
