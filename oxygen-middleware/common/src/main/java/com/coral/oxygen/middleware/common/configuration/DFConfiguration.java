package com.coral.oxygen.middleware.common.configuration;

import com.coral.oxygen.df.api.DFService;
import com.coral.oxygen.df.api.impl.DFServiceImpl;
import com.coral.oxygen.middleware.common.mappers.DFGreyhoundRacingOutcomeMapper;
import com.coral.oxygen.middleware.common.mappers.DFHorseRacingOutcomeMapper;
import com.coral.oxygen.middleware.pojos.model.Brand;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@Slf4j
public class DFConfiguration {

  @Bean
  @Qualifier("dfHttpClient")
  public OkHttpClient httpClient(
      OkHttpClientCreator okHttpClientCreator,
      DFConfigurationProperties properties,
      @Value("${http.proxyHost}") String proxyHost,
      @Value("${http.proxyPort}") String proxyPort)
      throws KeyManagementException, NoSuchAlgorithmException {
    return okHttpClientCreator.createOkHttpClient(
        properties.getTimeout().getConnect().getSeconds(),
        properties.getTimeout().getRead().getSeconds(),
        properties.getMaxIdleConnections(),
        properties.getKeepAliveDuration().getSeconds(),
        log::info,
        properties.getLogging().getLevel(),
        proxyHost,
        proxyPort);
  }

  @Bean
  public DFService getService(
      @Value("${df.url}") String baseUrl,
      @Value("${df.version}") String version,
      @Value("${df.apikey}") String apiKey,
      @Qualifier("dfHttpClient") OkHttpClient okHttpClient) {
    return new DFServiceImpl(baseUrl, version, apiKey, okHttpClient);
  }

  @Bean
  public DFHorseRacingOutcomeMapper getHorseRacingOutcomeMapper(
      @Value("${df.category.horse}") int categoryId) {
    return new DFHorseRacingOutcomeMapper(categoryId);
  }

  @Bean
  public DFGreyhoundRacingOutcomeMapper getGrayhoundOutcomeMapper(
      @Value("${df.category.greyhound}") int categoryId) {
    return new DFGreyhoundRacingOutcomeMapper(categoryId);
  }

  @Bean
  public Brand getBrand(@Value("${cms.brand}") String brand) {
    return Brand.from(brand);
  }
}
