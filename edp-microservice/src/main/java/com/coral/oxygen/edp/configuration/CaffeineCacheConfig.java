package com.coral.oxygen.edp.configuration;

import com.github.benmanes.caffeine.cache.Caffeine;
import java.util.Arrays;
import java.util.concurrent.TimeUnit;
import org.springframework.cache.CacheManager;
import org.springframework.cache.caffeine.CaffeineCache;
import org.springframework.cache.support.SimpleCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class CaffeineCacheConfig {

  public static final int DF_API_TIME = 3600;
  public static final int CMS_API_TIME = 90;

  @Bean
  public CacheManager cacheManager() {
    CaffeineCache dfHorseCache = buildCache("dfHorseInfo", DF_API_TIME);
    CaffeineCache dtoCache = buildCache("dto", CMS_API_TIME);
    SimpleCacheManager manager = new SimpleCacheManager();
    manager.setCaches(Arrays.asList(dfHorseCache, dtoCache));
    return manager;
  }

  public CaffeineCache buildCache(String name, int ttl) {
    return new CaffeineCache(
        name, Caffeine.newBuilder().expireAfterAccess(ttl, TimeUnit.SECONDS).build());
  }
}
