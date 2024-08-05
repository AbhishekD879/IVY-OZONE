package com.ladbrokescoral.reactions.config;

import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import java.time.Duration;
import java.util.concurrent.TimeUnit;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import reactor.netty.http.client.HttpClient;

/**
 * @author PBalarangakumar 15-06-2023
 */
@Configuration
public class HttpClientConfig {

  private final HttpClientPropertiesConfig httpClientPropertiesConfig;

  public HttpClientConfig(HttpClientPropertiesConfig httpClientPropertiesConfig) {
    this.httpClientPropertiesConfig = httpClientPropertiesConfig;
  }

  /**
   * httpClient will create httpClient Object and return
   *
   * @return httpClient
   */
  @Bean
  public HttpClient httpClient() {

    return HttpClient.create()
        .proxyWithSystemProperties()
        .compress(true)
        .responseTimeout(Duration.ofSeconds(httpClientPropertiesConfig.getResponseTimeout()))
        .option(
            ChannelOption.CONNECT_TIMEOUT_MILLIS, httpClientPropertiesConfig.getConnectTimeout())
        .option(ChannelOption.SO_KEEPALIVE, httpClientPropertiesConfig.isKeepAlive())
        .doOnConnected(
            connection ->
                connection.addHandlerFirst(
                    new ReadTimeoutHandler(
                        httpClientPropertiesConfig.getReadTimeout(), TimeUnit.SECONDS)));
  }
}
