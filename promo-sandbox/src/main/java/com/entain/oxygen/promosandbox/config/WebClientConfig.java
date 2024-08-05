package com.entain.oxygen.promosandbox.config;

import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import io.netty.handler.timeout.WriteTimeoutHandler;
import java.time.Duration;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.util.StringUtils;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;
import reactor.netty.resources.ConnectionProvider;
import reactor.netty.transport.ProxyProvider;

@Configuration
@Slf4j
public class WebClientConfig {

  @Value("${bpp.baseUrl}")
  private String baseUrl;

  @Value("${bpp.maxConnections}")
  private int maxConnections;

  @Value("${bpp.acquireTimeout}")
  private int acquireTimeout;

  @Value("${bpp.connectionTimeout}")
  private int connectionTimeout;

  @Value("${bpp.readTimeout}")
  private int readTimeout;

  @Value("${bpp.writeTimeout}")
  private int writeTimeout;

  @Bean
  public WebClient webclient() {
    ConnectionProvider provider =
        ConnectionProvider.builder("fixed")
            .maxConnections(maxConnections)
            .pendingAcquireTimeout(Duration.ofMillis(acquireTimeout))
            .build();

    log.info("proxy host" + System.getProperty("http.proxyHost"));
    log.info("proxy port" + System.getProperty("http.proxyPort"));
    String proxyHost = System.getProperty("http.proxyHost");
    String proxyPort = System.getProperty("http.proxyPort");

    String nonProxyHosts = System.getProperty("http.nonProxyHosts", "localhost");

    HttpClient httpClient;

    if (StringUtils.hasText(proxyHost) && StringUtils.hasText(proxyPort)) {
      httpClient =
          HttpClient.create(provider)
              .proxy(
                  proxy ->
                      proxy
                          .type(ProxyProvider.Proxy.HTTP)
                          .host(proxyHost)
                          .port(Integer.parseInt(proxyPort))
                          .nonProxyHosts(nonProxyHosts))
              .compress(true)
              .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, connectionTimeout)
              .doOnConnected(
                  con ->
                      con.addHandlerLast(new ReadTimeoutHandler(readTimeout))
                          .addHandlerLast(new WriteTimeoutHandler(writeTimeout)));
    } else {
      httpClient =
          HttpClient.create(provider)
              .compress(true)
              .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, connectionTimeout)
              .doOnConnected(
                  con ->
                      con.addHandlerLast(new ReadTimeoutHandler(readTimeout))
                          .addHandlerLast(new WriteTimeoutHandler(writeTimeout)));
    }

    return WebClient.builder()
        .baseUrl(baseUrl)
        .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
        .clientConnector(new ReactorClientHttpConnector(httpClient))
        .build();
  }
}
