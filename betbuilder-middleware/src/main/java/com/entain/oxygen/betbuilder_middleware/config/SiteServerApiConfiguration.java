package com.entain.oxygen.betbuilder_middleware.config;

import com.egalacoral.spark.siteserver.api.SiteServerApiAsync;
import com.egalacoral.spark.siteserver.api.SiteServerAsyncImpl;
import io.netty.channel.ChannelOption;
import java.util.function.UnaryOperator;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.ReactorResourceFactory;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import reactor.netty.http.client.HttpClient;
import reactor.netty.resources.ConnectionProvider;

@Configuration
public class SiteServerApiConfiguration {

  @Value("${site-server.base.url}")
  private String siteServerUrl;

  @Value("${site-server.api.version}")
  private String apiVersion;

  @Value("${site-server.read.timeout}")
  private int readTimeout;

  @Value("${site-server.use.epoll}")
  private boolean useEpoll;

  @Value("${site-server.threads}")
  private int numberOfThreads;

  @Value("${site-server.max-memory-size}")
  private int maxMemorySize;

  @Value("${site-server.max-connections}")
  private int maxConnections;

  @Value("${site-server.use-global-resources}")
  private boolean useGlobalResources;

  @Value("${site-server.compression-enabled}")
  private boolean compressionEnabled;

  @Value("${site-server.keep-alive}")
  private boolean keepAlive;

  @Value("${site-server.httpclient.threadMultiplier}")
  private int threadMultiplier;

  @Value("${site-server.wiretap.enabled}")
  private boolean isWiretapEnabled;

  @Value("${site-server.httpclient.threadKeepAliveSeconds}")
  private int threadKeepAliveSeconds;

  @Bean
  public SiteServerApiAsync siteServerAsync() {

    ReactorResourceFactory factory = new ReactorResourceFactory();
    ConnectionProvider provider = ConnectionProvider.create("SiteServerAsync", maxConnections);
    factory.setUseGlobalResources(useGlobalResources);
    factory.setConnectionProvider(provider);
    factory.afterPropertiesSet();

    UnaryOperator<HttpClient> mapper =
        client ->
            HttpClient.create(provider)
                .proxyWithSystemProperties()
                .compress(compressionEnabled)
                .keepAlive(keepAlive)
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, readTimeout)
                .wiretap(isWiretapEnabled)
                .runOn(
                    EventLoopConfigurer.getEventLoopGroup(
                        useEpoll,
                        "SiteServerAsync",
                        numberOfThreads,
                        threadMultiplier,
                        threadKeepAliveSeconds));

    ReactorClientHttpConnector connector = new ReactorClientHttpConnector(factory, mapper);
    return new SiteServerAsyncImpl(siteServerUrl, apiVersion, connector, maxMemorySize);
  }
}
