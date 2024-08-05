package com.entain.oxygen.configuration;

import com.github.benmanes.caffeine.cache.Caffeine;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.cache.CacheManager;
import org.springframework.cache.caffeine.CaffeineCache;
import org.springframework.cache.support.SimpleCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConditionalOnBean(value = {CustomCacheProperties.class})
@ConditionalOnProperty(name = "user-stable-cache.enabled", havingValue = "true")
@Slf4j
public class CachingConfiguration {

  @Bean
  public CacheManager cacheManager(CustomCacheProperties cacheProperties) {
    log.debug("cache built");
    List<CaffeineCache> cacheList =
        cacheProperties.getCaches().stream().map(this::buildCaches).collect(Collectors.toList());
    SimpleCacheManager simpleCacheManager = new SimpleCacheManager();
    simpleCacheManager.setCaches(cacheList);
    return simpleCacheManager;
  }

  private CaffeineCache buildCaches(CustomCacheProperties.CacheConfig cacheConfig) {
    return new CaffeineCache(
        cacheConfig.getCacheName(),
        Caffeine.newBuilder()
            .expireAfterWrite(cacheConfig.getTtl(), TimeUnit.valueOf(cacheConfig.getTimeUnit()))
            .build());
  }
}
