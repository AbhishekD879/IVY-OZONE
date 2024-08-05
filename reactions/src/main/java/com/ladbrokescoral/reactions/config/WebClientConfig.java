package com.ladbrokescoral.reactions.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;

/**
 * @author PBalarangakumar 16-06-2023
 */
@Configuration
public class WebClientConfig {

  private static final int BYTE_COUNT = 16 * 1024 * 1024;

  private final HttpClient httpClient;

  public WebClientConfig(final HttpClient httpClient) {
    this.httpClient = httpClient;
  }

  @Bean
  public WebClient webClient() {
    return WebClient.builder()
        .clientConnector(new ReactorClientHttpConnector(httpClient))
        .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
        .codecs(config -> config.defaultCodecs().maxInMemorySize(BYTE_COUNT))
        .build();
  }
}
