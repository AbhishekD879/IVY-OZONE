package com.ladbrokescoral.aggregation.configuration;

import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import io.netty.handler.timeout.WriteTimeoutHandler;
import java.time.Duration;
import java.util.function.UnaryOperator;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
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

@Slf4j
@Configuration
@Setter
public class WebClientConfig {

  private final ApiProperties apiProperties;
  private final int maxConnections;
  private final int acquireTimeout;

  @Value("${webclient.netty.use.pool:false}")
  private boolean usePool;

  @Value("${webclient.netty.use.epoll:false}")
  private boolean useEpoll;

  public WebClientConfig(
      ApiProperties apiProperties,
      @Value("${webclient.max.connections}") int maxConnections,
      @Value("${webclient.acquire.timeout}") int acquireTimeout) {

    this.apiProperties = apiProperties;
    this.maxConnections = maxConnections;
    this.acquireTimeout = acquireTimeout;
  }

  @Bean
  @Qualifier("providerWebClientForSilks")
  public WebClient providerWebClientForSilks(
      WebClient.Builder webClientBuilder, @Value("${webclient.silks.threads:0}") int maxThreads) {

    return getWebClientConfig(
        webClientBuilder,
        getConnectionProvider(usePool, maxConnections, acquireTimeout),
        "silks",
        maxThreads);
  }

  @Bean
  @Qualifier("providerWebClientForImages")
  public WebClient providerWebClientForImages(
      WebClient.Builder webClientBuilder, @Value("${webclient.images.threads:0}") int maxThreads) {

    return getWebClientConfig(
        webClientBuilder,
        getConnectionProvider(usePool, maxConnections, acquireTimeout),
        "silks",
        maxThreads);
  }

  private static ConnectionProvider getConnectionProvider(
      boolean usePool, int maxConnections, int acquireTimeout) {
    ConnectionProvider provider = null;
    if (!usePool) provider = ConnectionProvider.newConnection();
    else
      provider =
          ConnectionProvider.builder("fixed")
              .maxConnections(maxConnections)
              .pendingAcquireTimeout(Duration.ofMillis(acquireTimeout))
              .build();
    return provider;
  }

  private WebClient getWebClientConfig(
      WebClient.Builder webClientBuilder,
      ConnectionProvider provider,
      String poolName,
      int maxThreads) {
    ReactorResourceFactory factory = new ReactorResourceFactory();
    factory.setUseGlobalResources(false);
    factory.setConnectionProvider(provider);
    factory.afterPropertiesSet();

    UnaryOperator<HttpClient> mapper =
        client -> {
          return HttpClient.create(provider)
              .proxyWithSystemProperties()
              .compress(true)
              .runOn(EventLoopConfigurer.getEventLoopGroup(useEpoll, poolName, maxThreads))
              .option(
                  ChannelOption.CONNECT_TIMEOUT_MILLIS,
                  (int) apiProperties.getImage().getConnectionTimeout().toMillis())
              .option(ChannelOption.SO_KEEPALIVE, true)
              .doOnConnected(
                  con ->
                      con.addHandlerLast(
                              new ReadTimeoutHandler(
                                  (int) apiProperties.getImage().getReadTimeout().getSeconds()))
                          .addHandlerLast(
                              new WriteTimeoutHandler(
                                  (int) apiProperties.getImage().getWriteTimeout().getSeconds())));
        };

    return webClientBuilder
        .clientConnector(new ReactorClientHttpConnector(factory, mapper))
        .filter(
            (request, next) ->
                next.exchange(request)
                    .doOnNext(
                        r -> {
                          log.debug(
                              "Request >> {} {}, Headers >> {}",
                              request.method(),
                              request.url(),
                              request.headers());
                          log.debug(
                              "Response to {} << {} {}, Headers << {}",
                              request.url(),
                              r.statusCode().value(),
                              r.statusCode().getReasonPhrase(),
                              r.headers().asHttpHeaders());
                        }))
        .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
        .build();
  }
}
