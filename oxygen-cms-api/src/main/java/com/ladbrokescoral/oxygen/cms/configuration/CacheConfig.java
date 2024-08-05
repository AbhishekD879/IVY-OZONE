package com.ladbrokescoral.oxygen.cms.configuration;

import com.github.benmanes.caffeine.cache.Caffeine;
import com.github.benmanes.caffeine.cache.Ticker;
import java.util.*;
import java.util.concurrent.TimeUnit;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.cache.CacheManager;
import org.springframework.cache.caffeine.CaffeineCache;
import org.springframework.cache.support.SimpleCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties
public class CacheConfig {

  @Bean
  public CacheManager cacheManager(Ticker ticker, CustomCacheProperties cacheProperties) {
    List<CaffeineCache> caches = new ArrayList<>();
    for (Map.Entry<String, CustomCacheProperty> customCachePropertyEntry :
        cacheProperties.getCaches().entrySet()) {

      String cacheName = customCachePropertyEntry.getKey();
      CustomCacheProperty cacheProperty = customCachePropertyEntry.getValue();
      Objects.requireNonNull(cacheProperty);
      Objects.requireNonNull(cacheProperty.getTtl());

      caches.add(buildCache(cacheName, ticker, cacheProperty.getTtl()));
    }

    SimpleCacheManager simpleCacheManager = new SimpleCacheManager();
    simpleCacheManager.setCaches(caches);
    return simpleCacheManager;
  }

  private CaffeineCache buildCache(String cacheName, Ticker ticker, long minutesToExpire) {
    return new CaffeineCache(
        cacheName,
        Caffeine.newBuilder()
            .expireAfterWrite(minutesToExpire, TimeUnit.SECONDS)
            .ticker(ticker)
            .build());
  }

  @Bean
  public Ticker ticker() {
    return Ticker.systemTicker();
  }

  @Bean
  @ConfigurationProperties
  public CustomCacheProperties cacheProperties() {
    return new CustomCacheProperties();
  }

  /** Represents custom cache configuration from application.yaml */
  public static class CustomCacheProperties {
    private Map<String, CustomCacheProperty> caches = new HashMap<>();

    public Map<String, CustomCacheProperty> getCaches() {
      return caches;
    }
  }

  public static class CustomCacheProperty {
    private Long maxSize;
    private Long ttl;

    public Long getMaxSize() {
      return maxSize;
    }

    public void setMaxSize(Long maxSize) {
      this.maxSize = maxSize;
    }

    public Long getTtl() {
      return ttl;
    }

    public void setTtl(Long ttl) {
      this.ttl = ttl;
    }
  }
}
