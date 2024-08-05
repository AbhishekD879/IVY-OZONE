package com.ladbrokescoral.cashout.config;

import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import io.netty.handler.timeout.WriteTimeoutHandler;
import java.util.concurrent.TimeUnit;
import java.util.function.UnaryOperator;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.http.client.reactive.ReactorResourceFactory;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;
import reactor.netty.resources.ConnectionProvider;

@Configuration
public class WebClientConfig {

  @Value("${cashout.http.use.epoll:false}")
  private boolean useEpoll;

  @Value("${cashout.offer.http.threads:50}")
  private int numberOfThreads;

  @Bean("cashoutWebClient")
  public WebClient cashoutWebClient(
      @Value("${openbet.cashout.url}") String baseUrl,
      @Value("${openbet.cashout.connect.timeout}") int connectTimeout,
      @Value("${openbet.cashout.read.timeout}") int readTimeout,
      @Value("${openbet.cashout.write.timeout}") int writeTimeout,
      @Value("${cashout.offer.http.pool.size:50}") int poolSize) {

    ReactorResourceFactory factory = new ReactorResourceFactory();
    ConnectionProvider provider = ConnectionProvider.create("Cashout-Offer", poolSize);
    factory.setUseGlobalResources(false);
    factory.setConnectionProvider(provider);
    factory.afterPropertiesSet();

    UnaryOperator<HttpClient> mapper =
        client -> {
          return HttpClient.create(provider)
              .proxyWithSystemProperties()
              .compress(true)
              .keepAlive(true)
              .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, connectTimeout)
              .option(ChannelOption.SO_KEEPALIVE, true)
              .runOn(
                  EventLoopConfigurer.getEventLoopGroup(useEpoll, "Cashout-Offer", numberOfThreads))
              .doOnConnected(
                  conn ->
                      conn.addHandlerLast(
                              new ReadTimeoutHandler(readTimeout, TimeUnit.MILLISECONDS))
                          .addHandlerLast(
                              new WriteTimeoutHandler(writeTimeout, TimeUnit.MILLISECONDS)));
        };

    ReactorClientHttpConnector connector = new ReactorClientHttpConnector(factory, mapper);
    return WebClient.builder()
        .clientConnector(connector)
        .baseUrl(baseUrl)
        .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
        .build();
  }
}
