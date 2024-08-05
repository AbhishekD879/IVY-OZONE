package com.coral.oxygen.middleware.ms.quickbet.configuration;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.github.benmanes.caffeine.cache.Caffeine;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.TimeUnit;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.caffeine.CaffeineCache;
import org.springframework.cache.support.NoOpCacheManager;
import org.springframework.cache.support.SimpleCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Created by azayats on 13.10.17. */
@Configuration
@EnableCaching
public class SiteServerApiConfiguration {

  @Bean
  public SiteServerApi siteServerAPI(
      @Value("${siteServer.base.url}") String siteServerUrl,
      @Value("${siteServer.connection.timeout}") int connectionTimeout,
      @Value("${siteServer.read.timeout}") int readTimeout,
      @Value("${siteServer.retries.number}") int retriesNumber,
      @Value("${siteServer.logging.level}") String loggingLevel,
      @Value("${siteServer.pool.size}") int poolSize,
      @Value("${siteServer.keep.alive}") long keepAlive,
      @Value("${siteServer.api.version}") String apiVersion,
      @Value("${siteserver.api.latest.version}") String latestApiVersion,
      @Value("${siteserver.priceboost.enabled}") boolean isPriceBoostEnabled)
      throws NoSuchAlgorithmException, KeyManagementException {
    return new SiteServerApi.Builder()
        .setUrl(siteServerUrl)
        .setLoggingLevel(SiteServerApi.Level.valueOf(loggingLevel))
        .setConnectionTimeout(connectionTimeout)
        .setReadTimeout(readTimeout)
        .setMaxNumberOfRetries(retriesNumber)
        .setVersion(getapiVersion(apiVersion, latestApiVersion, isPriceBoostEnabled))
        .setConnectionPoolSettings(poolSize, keepAlive)
        .build();
  }

  @Bean
  @ConditionalOnProperty(
      name = "siteServer.cache.enabled",
      havingValue = "true",
      matchIfMissing = true)
  public CacheManager cacheManager(
      @Value("${siteServer.cache.ttl.sec}") int cacheTtl,
      @Value("${siteServer.cache.size}") int cacheSize,
      @Value("${siteServer.cache.cache-names}") String cacheNamesLine) {

    List<CaffeineCache> caches = new ArrayList<>();
    List<String> cacheNames = Arrays.asList(cacheNamesLine.split(","));
    cacheNames.forEach(name -> caches.add(buildCache(name, cacheSize, cacheTtl)));
    SimpleCacheManager cacheManager = new SimpleCacheManager();
    cacheManager.setCaches(caches);
    return cacheManager;
  }

  private CaffeineCache buildCache(String cacheName, long cacheSize, long cacheTtl) {
    return new CaffeineCache(
        cacheName,
        Caffeine.newBuilder()
            .expireAfterWrite(cacheTtl, TimeUnit.SECONDS)
            .maximumSize(cacheSize)
            .build());
  }

  @Bean
  @ConditionalOnProperty(name = "siteServer.cache.enabled", havingValue = "false")
  public CacheManager noOpCacheManager() {
    return new NoOpCacheManager();
  }

  private String getapiVersion(
      String apiVersion, String latestApiVersion, boolean isPriceBoostEnabled) {
    if (isPriceBoostEnabled) {
      return latestApiVersion;
    }
    return apiVersion;
  }
}
