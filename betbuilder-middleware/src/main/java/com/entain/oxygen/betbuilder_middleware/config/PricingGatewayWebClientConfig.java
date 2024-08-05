package com.entain.oxygen.betbuilder_middleware.config;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;

@Configuration
public class PricingGatewayWebClientConfig implements WebClientConfig {
  PricingGatewayClientProperties pricingGatewayClientProperties;

  public PricingGatewayWebClientConfig(
      PricingGatewayClientProperties pricingGatewayClientProperties) {
    this.pricingGatewayClientProperties = pricingGatewayClientProperties;
  }

  @Bean("pricingGatewayHttpClient")
  public HttpClient pricingGatewayHttpClient() {
    return buildHttpClient(pricingGatewayClientProperties);
  }

  @Bean("pricingGatewayWebClient")
  public WebClient pricingGatewayWebClient(
      @Qualifier("pricingGatewayHttpClient") HttpClient pricingGatewayHttpClient,
      PricingGatewayClientProperties pricingGatewayClientProperties) {
    return buildWebClient(pricingGatewayHttpClient, pricingGatewayClientProperties);
  }
}
