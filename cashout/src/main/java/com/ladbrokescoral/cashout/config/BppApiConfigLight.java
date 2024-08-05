package com.ladbrokescoral.cashout.config;

import com.coral.bpp.api.service.BppApiAsync;
import com.coral.bpp.api.service.impl.BppApiAsyncImpl;
import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import io.netty.handler.timeout.WriteTimeoutHandler;
import java.util.concurrent.TimeUnit;
import java.util.function.UnaryOperator;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.http.client.reactive.ReactorResourceFactory;
import reactor.netty.http.client.HttpClient;
import reactor.netty.resources.ConnectionProvider;

@Configuration
public class BppApiConfigLight {

  @Value("${bpp.api.url}")
  private String url;

  @Value("${bpp.light.retry.number}")
  private int retryNumber;

  @Value("${bpp.light.connect.timeout}")
  private int connectTimeout;

  @Value("${bpp.light.read.timeout}")
  private int readTimeout;

  @Value("${bpp.light.write.timeout}")
  private int writeTimeout;

  @Value("${bpp.light.retry.timeout}")
  private int retryTimeoutMillis;

  @Value("${bpp.light.pool.size}")
  private int poolSize = 1000;

  @Value("${bpp.light.pool.timeout}")
  private long poolTimeout = 45_000;

  @Value("${cashout.http.use.epoll:false}")
  private boolean useEpoll;

  @Value("${bpp.light.http.threads:50}")
  private int numberOfThreads;

  @Value("${bpp.maxInMemorySize:-1}")
  private int maxInMemorySize;

  @Bean
  public BppApiAsync bppApiAsyncLight() {

    ReactorResourceFactory factory = new ReactorResourceFactory();
    ConnectionProvider provider = ConnectionProvider.create("bppLightPool", poolSize);
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
              // .wiretap("reactor.netty.http.client.HttpClient", LogLevel.ERROR)
              .runOn(EventLoopConfigurer.getEventLoopGroup(useEpoll, "Bpp-Light", numberOfThreads))
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
