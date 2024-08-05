package com.ladbrokescoral.oxygen.seo.configuration;

import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import io.netty.handler.timeout.WriteTimeoutHandler;
import java.util.concurrent.TimeUnit;
import java.util.function.UnaryOperator;
import lombok.Setter;
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
@Setter
public class CmsWebClientConfig {

  @Value("${cms.http.use.epoll:false}")
  private boolean useEpoll;

  @Value("${cms.http.threads:50}")
  private int numberOfThreads;

  @Value("${cms.http.pool.size:50}")
  private int poolSize;

  @Value("${cms.timout.read:1000}")
  int readTimeout;

  @Value("${cms.timout.write:1000}")
  int writeTimeout;

  @Value("${cms.timout.connect:3000}")
  int connectTimeout;

  @Value("${cms.base.url}")
  String baseUrl;

  @Bean
  public WebClient cmsWebClient() {

    ReactorResourceFactory factory = new ReactorResourceFactory();
    ConnectionProvider provider = ConnectionProvider.create("CMS-API", poolSize);
    factory.setUseGlobalResources(false);
    factory.setConnectionProvider(provider);
    factory.afterPropertiesSet();

    UnaryOperator<HttpClient> mapper =
        client ->
            HttpClient.create(provider)
                .proxyWithSystemProperties()
                .compress(true)
                .keepAlive(true)
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, connectTimeout)
                .option(ChannelOption.SO_KEEPALIVE, true)
                .runOn(EventLoopConfigurer.getEventLoopGroup(useEpoll, "CMS-API", numberOfThreads))
                .doOnConnected(
                    conn ->
                        conn.addHandlerLast(
                                new ReadTimeoutHandler(readTimeout, TimeUnit.MILLISECONDS))
                            .addHandlerLast(
                                new WriteTimeoutHandler(writeTimeout, TimeUnit.MILLISECONDS)));

    ReactorClientHttpConnector connector = new ReactorClientHttpConnector(factory, mapper);
    return WebClient.builder()
        .clientConnector(connector)
        .baseUrl(baseUrl)
        .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
        .build();
  }
}
