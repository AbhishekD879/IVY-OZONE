package com.ladbrokescoral.oxygen.seo.configuration;

import com.egalacoral.spark.siteserver.api.SiteServerApiAsync;
import com.egalacoral.spark.siteserver.api.SiteServerAsyncImpl;
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
public class SiteServerApiConfiguration {
  @Value("${siteServer.base.url}")
  private String siteServerUrl;

  @Value("${siteserver.api.version}")
  private String apiVersion;

  @Value("${siteserver.connection.timeout}")
  private int connectionTimeout;

  @Value("${siteserver.read.timeout}")
  private int readTimeout;

  @Value("${siteserver.write.timeout}")
  private int writeTimeout;

  @Value("${siteserver.logging.level}")
  private String loggingLevel;

  @Value("${siteserver.use.epoll:false}")
  private boolean useEpoll;

  @Value("${siteserver.pool.size:50}")
  private int poolSize;

  @Value("${siteserver.threads:50}")
  private int numberOfThreads;

  @Value("${siteserver.max-memory-size:16777216}")
  private int maxMemorySize;

  @Bean
  public SiteServerApiAsync siteServerAsync() {

    ReactorResourceFactory factory = new ReactorResourceFactory();
    ConnectionProvider provider = ConnectionProvider.create("SiteServerAsync", poolSize);
    factory.setUseGlobalResources(false);
    factory.setConnectionProvider(provider);
    factory.afterPropertiesSet();

    UnaryOperator<HttpClient> mapper =
        client ->
            HttpClient.create(provider)
                .proxyWithSystemProperties()
                .compress(true)
                .keepAlive(true)
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, readTimeout)
                .option(ChannelOption.SO_KEEPALIVE, true)
                .runOn(
                    EventLoopConfigurer.getEventLoopGroup(
                        useEpoll, "SiteServerAsync", numberOfThreads))
                .doOnConnected(
                    conn ->
                        conn.addHandlerLast(
                                new ReadTimeoutHandler(readTimeout, TimeUnit.MILLISECONDS))
                            .addHandlerLast(
                                new WriteTimeoutHandler(writeTimeout, TimeUnit.MILLISECONDS)));

    ReactorClientHttpConnector connector = new ReactorClientHttpConnector(factory, mapper);
    return new SiteServerAsyncImpl(siteServerUrl, apiVersion, connector, maxMemorySize);
  }
}
