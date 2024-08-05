package com.ladbrokescoral.oxygen.questionengine.configuration;

import com.github.benmanes.caffeine.cache.Caffeine;
import com.ladbrokescoral.oxygen.questionengine.configuration.properties.ApplicationProperties;
import lombok.RequiredArgsConstructor;
import org.springframework.cache.caffeine.CaffeineCache;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.TimeUnit;

@Configuration
@RequiredArgsConstructor
public class CacheConfiguration {
  private final ApplicationProperties properties;

  @Bean
  public CaffeineCache upsellCache() {
    return new CaffeineCache("upsellCache",
        Caffeine.newBuilder()
            .expireAfterWrite(properties.getUpsellCacheTtlMinutes(), TimeUnit.MINUTES)
            .build()
    );
  }

  @Bean
  public CaffeineCache quizHistoryCache() {
    return new CaffeineCache("quizHistoryCache",
        Caffeine.newBuilder()
            .expireAfterWrite(properties.getHistoryCacheTtlDays(), TimeUnit.DAYS)
            .build()
    );
  }

  @Bean
  public CaffeineCache liveQuizCache() {
    return new CaffeineCache("liveQuizCache",
        Caffeine.newBuilder()
            .expireAfterWrite(properties.getLiveQuizCacheTtlDays(), TimeUnit.DAYS)
            .build()
    );
  }

  @Bean
  public CaffeineCache cmsHistoryQuizzesCache() {
    return new CaffeineCache("cmsHistoryQuizzesCache",
            Caffeine.newBuilder()
                    .expireAfterWrite(properties.getHistoryCacheTtlDays(), TimeUnit.DAYS)
                    .build()
    );
  }
}
