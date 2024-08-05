package com.coral.oxygen.middleware.common.configuration;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.cms.api.SystemConfigProvider;
import com.coral.oxygen.cms.api.impl.CachedSystemConfigProvider;
import com.coral.oxygen.cms.api.impl.CmsServiceImpl;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Slf4j(topic = "CMSOkHttp")
@Configuration
public class CmsConfiguration {

  private static final int MAX_IDLE_CONNECTIONS = 1;
  private static final int KEEP_ALIVE_DURATION = 60;
  private static final String PROXY_HOST = null;
  private static final String PROXY_PORT = null;

  @Bean
  public OkHttpClient cmsOkHttpClient(
      @Value("${cms.timout.read:2}") int readTimeout,
      @Value("${cms.timout.connect:2}") int connectTimeout,
      @Value("${cms.logging.level:BASIC}") String cmsLoggingLevel,
      OkHttpClientCreator okHttpClientCreator)
      throws KeyManagementException, NoSuchAlgorithmException {
    // Changed from 1 to 60 bc changed timeunit for keepAliveDuration to SECONDS in
    // OkHttpClientCreator.createOkHttpClient
    return okHttpClientCreator.createOkHttpClient(
        connectTimeout,
        readTimeout,
        MAX_IDLE_CONNECTIONS,
        KEEP_ALIVE_DURATION,
        log::info,
        cmsLoggingLevel,
        PROXY_HOST,
        PROXY_PORT);
  }

  @Bean
  public CmsService getCmsService(
      @Value("${cms.url}") String baseUrl,
      @Qualifier("cmsOkHttpClient") OkHttpClient okHttpClient) {
    return new CmsServiceImpl(baseUrl, okHttpClient);
  }

  @Bean
  public SystemConfigProvider systemConfigProvider(CmsService cmsService) {
    return new CachedSystemConfigProvider(cmsService, 5);
  }
}
