package com.entain.oxygen.configuration;

import java.util.List;
import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "user-stable-cache")
@Data
public class CustomCacheProperties {

  private List<CacheConfig> caches;

  @Data
  public static class CacheConfig {
    private String cacheName;
    private Long ttl;
    private String timeUnit;
  }
}
