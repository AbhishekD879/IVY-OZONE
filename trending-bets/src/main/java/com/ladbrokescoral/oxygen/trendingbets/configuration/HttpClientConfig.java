package com.ladbrokescoral.oxygen.trendingbets.configuration;

import io.netty.channel.ChannelOption;
import io.netty.channel.epoll.EpollChannelOption;
import io.netty.channel.socket.nio.NioChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import java.util.concurrent.TimeUnit;
import jdk.net.ExtendedSocketOptions;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import reactor.netty.http.client.HttpClient;
import reactor.netty.resources.ConnectionProvider;

@Configuration
@EnableConfigurationProperties(HttpClientProperties.class)
public class HttpClientConfig {

  @Setter
  @Value("${app.workerCount:100}")
  private int workerCount;

  @Value("${app.pool.use.epoll:false}")
  private boolean useEpoll;

  @Value("${app.http.threads:0}")
  private int numberOfThreads;

  @Value("${https.proxyHost}")
  private String proxyHost;

  @Value("${https.proxyPort:0}")
  private int proxyPort;

  private final HttpClientProperties httpClientProperties;

  public HttpClientConfig(HttpClientProperties httpClientProperties) {
    this.httpClientProperties = httpClientProperties;
  }

  @Bean
  public HttpClient httpClient() {
    HttpClient httpClient = HttpClient.create(connectionProvider());

    return httpClient
        .proxyWithSystemProperties()
        .compress(true)
        .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, httpClientProperties.getConnectTimeout())
        .option(ChannelOption.SO_KEEPALIVE, httpClientProperties.isKeepAlive())
        .option(
            NioChannelOption.of(ExtendedSocketOptions.TCP_KEEPIDLE),
            httpClientProperties.getTcpKeepIdle())
        .option(
            NioChannelOption.of(ExtendedSocketOptions.TCP_KEEPINTERVAL),
            httpClientProperties.getKeepInterval())
        .option(
            NioChannelOption.of(ExtendedSocketOptions.TCP_KEEPCOUNT),
            httpClientProperties.getKeepCount())
        // The connection needs to remain idle for 5 minutes before TCP starts sending keepalive
        // probes
        .option(EpollChannelOption.TCP_KEEPIDLE, httpClientProperties.getTcpKeepIdle())
        //	Configures the time between individual keepalive probes to 1 minute.
        .option(EpollChannelOption.TCP_KEEPINTVL, httpClientProperties.getKeepInterval())
        // Configures the maximum number of TCP keepalive probes to 8
        .option(EpollChannelOption.TCP_KEEPCNT, httpClientProperties.getKeepCount())
        .runOn(EventLoopHelper.getEventLoopGroup(useEpoll, "trending-bets", numberOfThreads))
        .doOnConnected(
            connection ->
                connection.addHandlerLast(
                    new ReadTimeoutHandler(
                        httpClientProperties.getReadTimeout(), TimeUnit.SECONDS)));
  }

  public ConnectionProvider connectionProvider() {

    return ConnectionProvider.builder("trending-bets")
        .maxConnections(httpClientProperties.getDefaultClientMaxConnections())
        .maxIdleTime(httpClientProperties.getMaxIdleTime())
        .maxLifeTime(httpClientProperties.getMaxLifeTime())
        .pendingAcquireTimeout(httpClientProperties.getPendingAcquireTimeout())
        .evictInBackground(httpClientProperties.getEvictInBackground())
        .build();
  }
}
