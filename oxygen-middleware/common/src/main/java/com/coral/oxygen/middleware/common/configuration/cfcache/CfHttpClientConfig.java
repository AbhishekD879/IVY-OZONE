package com.coral.oxygen.middleware.common.configuration.cfcache;

import com.coral.oxygen.middleware.common.configuration.OkHttpClientCreator;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Slf4j
@Configuration
public class CfHttpClientConfig {

  @Bean
  public OkHttpClient cfOkHttpClient(
      @Value("${cf.http.timeout.read:2}") int readTimeout,
      @Value("${cf.http.timeout.connect:2}") int connectTimeout,
      @Value("${cf.http.logging.level:BASIC}") String cmsLoggingLevel,
      @Value("${cf.http.maxIdleConnections}") int idleConnections,
      @Value("${cf.http.keepAliveDuration}") long keepAliveSeconds,
      @Value("${http.proxyHost}") String proxyHost,
      @Value("${http.proxyPort}") String proxyPort,
      OkHttpClientCreator okHttpClientCreator)
      throws NoSuchAlgorithmException, KeyManagementException {
    return okHttpClientCreator.createOkHttpClient(
        connectTimeout,
        readTimeout,
        idleConnections,
        keepAliveSeconds,
        log::info,
        cmsLoggingLevel,
        proxyHost,
        proxyPort);
  }
}
