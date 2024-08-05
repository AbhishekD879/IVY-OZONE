package com.oxygen.publisher.sportsfeatured.configuration;

import com.oxygen.publisher.model.ApplicationVersion;
import com.oxygen.publisher.sportsfeatured.SportsHealthIndicator;
import com.oxygen.publisher.sportsfeatured.SportsServiceRegistry;
import com.oxygen.publisher.sportsfeatured.context.SportsMiddlewareContext;
import com.oxygen.publisher.sportsfeatured.context.SportsSessionContext;
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import com.oxygen.publisher.sportsfeatured.service.FeaturedService;
import com.oxygen.publisher.sportsfeatured.service.FeaturedServiceImpl;
import okhttp3.Interceptor;
import okhttp3.logging.HttpLoggingInterceptor;
import okhttp3.logging.HttpLoggingInterceptor.Level;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Created by Aliaksei Yarotski on 12/22/17. */
@Configuration
public class FeaturedServiceConfiguration {

  @Bean
  public FeaturedService featuredService(SportsServiceRegistry serviceRegistry) {
    FeaturedServiceImpl service = new FeaturedServiceImpl();
    service.setServiceRegistry(serviceRegistry);
    return service;
  }

  @Bean
  public SportsMiddlewareContext middlewareContext(
      SportsServiceRegistry serviceRegistry, SportsCachedData sportsCachedData) {
    return new SportsMiddlewareContext(serviceRegistry, sportsCachedData);
  }

  @Bean
  public SportsCachedData sportsCachedData(
      @Value("${cache.structure.size:100}") int structureCacheSize,
      @Value("${tt.cache.second:180}") long ttlSeconds) {

    return new SportsCachedData(structureCacheSize, ttlSeconds);
  }

  @Bean
  public ApplicationVersion applicationVersion(@Value("${publisher.version}") String appVersion) {
    return new ApplicationVersion(appVersion);
  }

  @Bean
  public SportsSessionContext featuredSessionContext(
      ApplicationVersion applicationVersion, SportsMiddlewareContext featuredMiddlewareContext) {
    return new SportsSessionContext(applicationVersion, featuredMiddlewareContext);
  }

  @Bean
  public SportsHealthIndicator inplayHealthIndicator(
      SportsMiddlewareContext featuredMiddlewareContext, SportsServiceRegistry serviceRegistry) {
    return new SportsHealthIndicator(serviceRegistry, featuredMiddlewareContext);
  }

  @Bean
  public Interceptor loggingInterceptor(
      @Value("${featured.consumer.logging.level}") String loggingLevel) {
    HttpLoggingInterceptor loggingInteceptor =
        new HttpLoggingInterceptor(LoggerFactory.getLogger("FEAT-API")::info);
    loggingInteceptor.setLevel(Level.valueOf(loggingLevel));
    return loggingInteceptor;
  }
}
