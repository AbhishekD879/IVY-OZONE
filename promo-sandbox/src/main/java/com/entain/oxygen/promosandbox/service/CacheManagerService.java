package com.entain.oxygen.promosandbox.service;

import java.util.Objects;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.CacheManager;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class CacheManagerService {

  private final CacheManager cacheManager;

  public CacheManagerService(CacheManager cacheManager) {
    this.cacheManager = cacheManager;
  }

  public void clearCache() {
    cacheManager
        .getCacheNames()
        .forEach(
            (String cacheName) -> {
              log.info("Cache name : {} ", cacheName);
              Objects.requireNonNull(cacheManager.getCache(cacheName)).clear();
            });
    log.info("All cache data got cleared");
  }
}
