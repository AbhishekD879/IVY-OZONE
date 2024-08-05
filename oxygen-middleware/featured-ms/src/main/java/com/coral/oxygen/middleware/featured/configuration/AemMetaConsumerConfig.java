package com.coral.oxygen.middleware.featured.configuration;

import com.coral.oxygen.middleware.common.configuration.OkHttpClientCreator;
import com.coral.oxygen.middleware.featured.aem.AemMetaConsumer;
import com.coral.oxygen.middleware.featured.consumer.sportpage.AemCarouselsProcessor;
import java.io.IOException;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

@Slf4j
@Configuration
@Profile("AEM")
@ConfigurationProperties(prefix = "oxygen")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class AemMetaConsumerConfig {

  public static final int MAX_IDLE_CONNECTIONS = 1;
  public static final int KEEP_ALIVE_DURATION = 60;
  private List<SportsCategoriesLookup> sportsCategoriesLookup;

  @Bean(name = "aemOkHttpClient")
  public OkHttpClient cmsOkHttpClient(
      @Value("${aem.timout.read:2}") int readTimeout,
      @Value("${aem.timout.connect:2}") int connectTimeout,
      @Value("${aem.logging.level:BASIC}") String aemLoggingLevel,
      OkHttpClientCreator okHttpClientCreator,
      @Value("${http.proxyHost:}") String proxyHost,
      @Value("${http.proxyPort:}") String proxyPort)
      throws KeyManagementException, NoSuchAlgorithmException {

    return okHttpClientCreator.createOkHttpClient(
        connectTimeout,
        readTimeout,
        MAX_IDLE_CONNECTIONS,
        KEEP_ALIVE_DURATION,
        log::info,
        aemLoggingLevel,
        proxyHost,
        proxyPort);
  }

  @Bean
  public AemCarouselsProcessor aemCarouselsProcessor(AemMetaConsumer aemMetaConsumer)
      throws IOException {
    return new AemCarouselsProcessor(aemMetaConsumer, getSportsCategoriesDict());
  }

  @Bean
  public AemMetaConsumer aemMetaConsumer(
      @Value("${aem.offer.endpoint}") String baseUrl,
      @Value("${tenant-name}") String brandName,
      @Qualifier("aemOkHttpClient") OkHttpClient okHttpClient) {
    return new AemMetaConsumer(baseUrl, brandName, okHttpClient);
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class SportsCategoriesLookup {

    String categoryId;
    String[] synonyms;
  }

  protected Map<String, String> getSportsCategoriesDict() {
    log.info("Dict count: {} ", sportsCategoriesLookup);
    Map<String, String> result =
        sportsCategoriesLookup.stream()
            .collect(Collectors.toMap(lookup -> lookup.synonyms, lookup -> lookup.categoryId))
            .entrySet()
            .stream()
            .flatMap(
                entity ->
                    Arrays.stream(entity.getKey())
                        .collect(Collectors.toMap(cat -> cat, cat -> entity.getValue()))
                        .entrySet()
                        .stream())
            .collect(Collectors.toMap(entity -> entity.getKey(), entity -> entity.getValue()));
    return result;
  }
}
