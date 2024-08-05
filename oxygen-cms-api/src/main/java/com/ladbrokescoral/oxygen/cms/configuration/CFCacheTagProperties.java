package com.ladbrokescoral.oxygen.cms.configuration;

import java.util.Map;
import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@ConfigurationProperties(prefix = "cfcache")
@Data
@Component
public class CFCacheTagProperties {
  private Map<String, String> tags;
}
