package com.ladbrokescoral.cashout.config;

import com.coral.bpp.api.service.BppApiAsync;
import com.coral.bpp.api.service.impl.BppApiAsyncImpl;
import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import io.netty.handler.timeout.WriteTimeoutHandler;
import java.time.Duration;
import java.util.concurrent.TimeUnit;
import java.util.function.UnaryOperator;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.http.client.reactive.ReactorResourceFactory;
import reactor.netty.http.client.HttpClient;
import reactor.netty.resources.ConnectionProvider;

@Configuration
@Setter
public class BppApiConfigHeavy {

  @Value("${bpp.api.url}")
  private String url;

  @Value("${bpp.heavy.retry.number}")
  private int retryNumber;

  @Value("${bpp.heavy.connect.timeout}")
  private int connectTimeout;

  @Value("${bpp.heavy.read.timeout}")
  private int readTimeout;

  @Value("${bpp.heavy.write.timeout}")
  private int writeTimeout;

  @Value("${bpp.heavy.retry.timeout}")
  private int retryTimeoutMillis;

  @Value("${bpp.heavy.pool.size:1000}")
  private int poolSize;

  @Value("${bpp.heavy.pool.timeout}")
  private long poolTimeout = 45_000;

  @Value("${bpp.heavy.pool.use.epoll:false}")
  private boolean useEpoll;

  @Value("${bpp.heavy.http.threads:50}")
  private int numberOfThreads;

  @Value("${bpp.heavy.pool.keep.alive:false}")
  private boolean useKeepAlive;

  @Value("${cashout.host-address:localhost}")
  private String cashoutHostAddress;

  @Value("${bpp.heavy.maxIdleTime:20}")
  private int maxIdleTime;

  @Value("${bpp.heavy.maxLifeTime:60}")
  private int maxLifeTime;

  @Value("${bpp.heavy.pendingAcquireTimeout:60}")
  private int pendingAcquireTimeout;

  @Value("${bpp.heavy.evictInBackground:120}")
  private int evictInBackground;

  @Value("${bpp.maxInMemorySize:-1}")
  private int maxInMemorySize;

  @Bean
  public BppApiAsync bppApiAsyncHeavy() {

    ConnectionProvider provider =
        ConnectionProvider.builder("bppHeavyPool")
            .maxConnections(poolSize)
            .maxIdleTime(Duration.ofSeconds(maxIdleTime))
            .maxLifeTime(Duration.ofSeconds(maxLifeTime))
            .pendingAcquireTimeout(Duration.ofSeconds(pendingAcquireTimeout))
            .evictInBackground(Duration.ofSeconds(evictInBackground))
            .build();
    ReactorResourceFactory factory = new ReactorResourceFactory();
    factory.setUseGlobalResources(false);
    factory.setConnectionProvider(provider);
    factory.afterPropertiesSet();

    UnaryOperator<HttpClient> mapper =
        client -> {
          return HttpClient.create(provider)
              .headers(header -> header.add("cashoutHostAddress", cashoutHostAddress))
              .proxyWithSystemProperties()
              .compress(true)
              .keepAlive(useKeepAlive)
              .option(ChannelOption.TCP_NODELAY, true)
              .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, connectTimeout)
              .option(ChannelOption.SO_KEEPALIVE, useKeepAlive)
              // .wiretap("reactor.netty.http.client.HttpClient", LogLevel.ERROR)
              .runOn(EventLoopConfigurer.getEventLoopGroup(useEpoll, "Bpp-Heavy", numberOfThreads))
              .doOnConnected(
                  conn ->
                      conn.addHandlerLast(
                              new ReadTimeoutHandler(readTimeout, TimeUnit.MILLISECONDS))
                          .addHandlerLast(
                              new WriteTimeoutHandler(writeTimeout, TimeUnit.MILLISECONDS)));
        };

    return new BppApiAsyncImpl(
        url,
        retryNumber,
        retryTimeoutMillis,
        new ReactorClientHttpConnector(factory, mapper),
        maxInMemorySize);
  }
}
