package com.entain.oxygen.betbuilder_middleware.config;

import io.netty.channel.ChannelOption;
import io.netty.channel.epoll.EpollChannelOption;
import io.netty.channel.socket.nio.NioChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import io.netty.handler.timeout.WriteTimeoutHandler;
import java.time.Duration;
import java.util.concurrent.TimeUnit;
import jdk.net.ExtendedSocketOptions;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.ReactorResourceFactory;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;
import reactor.netty.resources.ConnectionProvider;

@Configuration
public interface WebClientConfig {
  public static final String CONTENT_TYPE = "Content-Type";

  public default WebClient buildWebClient(
      HttpClient defaultClient, WebClientProperties clientProperties) {
    return WebClient.builder()
        .baseUrl(clientProperties.getBaseUrl())
        .clientConnector(new ReactorClientHttpConnector(defaultClient))
        .codecs(
            configure ->
                configure.defaultCodecs().maxInMemorySize(clientProperties.getMaxInMemorySize()))
        .defaultHeader(CONTENT_TYPE, clientProperties.getContentType())
        .build();
  }

  public default HttpClient buildHttpClient(WebClientProperties clientProperties) {
    ReactorResourceFactory factory = new ReactorResourceFactory();
    ConnectionProvider provider =
        ConnectionProvider.builder(clientProperties.getConnectionName())
            .maxConnections(clientProperties.getMaxConnections())
            .pendingAcquireMaxCount(clientProperties.getPendingAcquireMaxCount())
            .pendingAcquireTimeout(Duration.ofSeconds(clientProperties.getPendingAcquireTimeout()))
            .maxIdleTime(Duration.ofSeconds(clientProperties.getMaxIdleTime()))
            .maxLifeTime(Duration.ofSeconds(clientProperties.getMaxLifeTime()))
            .evictInBackground(Duration.ofSeconds(clientProperties.getEvictInBackground()))
            .build();
    factory.setUseGlobalResources(clientProperties.isUseGlobalResources());
    factory.setConnectionProvider(provider);
    factory.afterPropertiesSet();
    return HttpClient.create(factory.getConnectionProvider())
        .compress(clientProperties.isCompressionEnabled())
        .keepAlive(clientProperties.isKeepAlive())
        .wiretap(clientProperties.isWiretapEnabled())
        .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, clientProperties.getConnectionTimeoutMillis())
        .option(ChannelOption.TCP_NODELAY, true)
        .option(
            NioChannelOption.of(ExtendedSocketOptions.TCP_KEEPIDLE),
            clientProperties.getTcpKeepIdle())
        .option(
            NioChannelOption.of(ExtendedSocketOptions.TCP_KEEPINTERVAL),
            clientProperties.getTcpKeepInterval())
        .option(
            NioChannelOption.of(ExtendedSocketOptions.TCP_KEEPCOUNT),
            clientProperties.getTcpKeepCount())
        // The connection needs to remain idle for 5 minutes before TCP starts sending keepalive
        // probes
        .option(EpollChannelOption.TCP_KEEPIDLE, clientProperties.getTcpKeepIdle())
        //	Configures the time between individual keepalive probes to 1 minute.
        .option(EpollChannelOption.TCP_KEEPINTVL, clientProperties.getTcpKeepInterval())
        // Configures the maximum number of TCP keepalive probes to 8
        .option(EpollChannelOption.TCP_KEEPCNT, clientProperties.getTcpKeepCount())
        .runOn(
            EventLoopConfigurer.getEventLoopGroup(
                clientProperties.isUseEpoll(),
                clientProperties.getThreadNamePrefix(),
                clientProperties.getNumberOfThreads(),
                clientProperties.getThreadMultiplier(),
                clientProperties.getThreadKeepAliveSeconds()))
        .doOnConnected(
            conn ->
                conn.addHandlerLast(
                        new ReadTimeoutHandler(
                            clientProperties.getReadTimeoutMillis(), TimeUnit.MILLISECONDS))
                    .addHandlerLast(
                        new WriteTimeoutHandler(
                            clientProperties.getWriteTimeoutMillis(), TimeUnit.MILLISECONDS)));
  }
}
