package com.ladbrokescoral.oxygen.trendingbets.configuration;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;

@Configuration
public class WebClientConfig {

  private final HttpClient httpClient;

  public WebClientConfig(final HttpClient httpClient) {
    this.httpClient = httpClient;
  }

  @Bean("adaWebClient")
  public WebClient adaWebClient() {
    return WebClient.builder()
        .clientConnector(new ReactorClientHttpConnector(httpClient))
        .codecs(configurer -> configurer.defaultCodecs().maxInMemorySize(-1))
        .build();
  }
}
