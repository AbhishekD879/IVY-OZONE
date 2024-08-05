package com.coral.oxygen.middleware.common.configuration;

import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.reflections.Reflections;
import org.reflections.scanners.MethodAnnotationsScanner;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.caffeine.CaffeineCache;
import org.springframework.cache.support.SimpleCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableCaching
@Slf4j
public class CachingConfiguration {

  private static final int EXPIRATION_TIME = 2500;

  @Value("${application.virtualSportCacheTTL}")
  private long virtualSportCacheTTL;

  @Value("${application.virtualSports.timeUnit}")
  private String timeUnit;

  private static final String VIRTUAL_SPORT_CACHE = "virtualSportsCache";

  @Bean
  public CacheManager cacheManager() {
    SimpleCacheManager cacheManager = new SimpleCacheManager();
    Cache<Object, Object> cache =
        Caffeine.newBuilder().expireAfterWrite(EXPIRATION_TIME, TimeUnit.MILLISECONDS).build();
    List<String> caches =
        getCachableNamesForPackage("com.coral.oxygen.middleware.featured.controller");
    caches.addAll(getCachableNamesForPackage("com.coral.oxygen.middleware.controller"));
    List<CaffeineCache> caffeineCaches =
        caches.stream().map(name -> new CaffeineCache(name, cache)).collect(Collectors.toList());
    caffeineCaches.add(virtualSportsCache());
    cacheManager.setCaches(caffeineCaches);
    return cacheManager;
  }

  public CaffeineCache virtualSportsCache() {
    log.info("virtualSportsCache Created ");
    return new CaffeineCache(
        VIRTUAL_SPORT_CACHE,
        Caffeine.newBuilder()
            .expireAfterWrite(virtualSportCacheTTL, TimeUnit.valueOf(timeUnit))
            .build());
  }

  private List<String> getCachableNamesForPackage(String packageName) {
    Reflections reflections = new Reflections(packageName, new MethodAnnotationsScanner());
    Set<Method> methodsAnnotatedWithCacheable =
        reflections.getMethodsAnnotatedWith(Cacheable.class);
    return methodsAnnotatedWithCacheable.stream()
        .map(method -> method.getAnnotation(Cacheable.class).value()[0])
        .collect(Collectors.toCollection(ArrayList::new));
  }
}
