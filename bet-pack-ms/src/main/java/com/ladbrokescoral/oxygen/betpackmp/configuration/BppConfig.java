package com.ladbrokescoral.oxygen.betpackmp.configuration;

import com.coral.bpp.api.service.BppApiAsync;
import com.coral.bpp.api.service.impl.BppApiAsyncImpl;
import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import io.netty.handler.timeout.WriteTimeoutHandler;
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
public class BppConfig {

  public static final int POOL_SIZE = 1000;
  public static final int POOL_TIME_OUT = 45_000;

  @Value("${bpp.url}")
  private String url;

  @Value("${bpp.retry.number}")
  private int retryNumber;

  @Value("${bpp.connect.timeout}")
  private int connectTimeout;

  @Value("${bpp.read.timeout}")
  private int readTimeout;

  @Value("${bpp.write.timeout}")
  private int writeTimeout;

  @Value("${bpp.retry.timeout}")
  private int retryTimeoutMillis;

  @Value("${bpp.pool.size}")
  private int poolSize = POOL_SIZE;

  @Value("${bpp.pool.timeout}")
  private long poolTimeout = POOL_TIME_OUT;

  @Value("${bpp.pool.use.epoll:false}")
  private boolean useEpoll;

  @Value("${bpp.http.threads:50}")
  private int numberOfThreads;

  @Value("${bpp.pool.keep.alive:false}")
  private boolean useKeepAlive;

  @Bean
  public BppApiAsync bppApiAsync() {

    ReactorResourceFactory factory = new ReactorResourceFactory();
    ConnectionProvider provider = ConnectionProvider.create("bppPool", poolSize);
    factory.setUseGlobalResources(false);
    factory.setConnectionProvider(provider);
    factory.afterPropertiesSet();

    UnaryOperator<HttpClient> mapper =
        client ->
            HttpClient.create(provider)
                .proxyWithSystemProperties()
                .compress(true)
                .keepAlive(useKeepAlive)
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, connectTimeout)
                .option(ChannelOption.SO_KEEPALIVE, useKeepAlive)
                .runOn(EventLoopConfigure.getEventLoopGroup(useEpoll, "Bpp", numberOfThreads))
                .doOnConnected(
                    conn ->
                        conn.addHandlerLast(
                                new ReadTimeoutHandler(readTimeout, TimeUnit.MILLISECONDS))
                            .addHandlerLast(
                                new WriteTimeoutHandler(writeTimeout, TimeUnit.MILLISECONDS)));

    return new BppApiAsyncImpl(
        url, retryNumber, retryTimeoutMillis, new ReactorClientHttpConnector(factory, mapper));
  }
}
