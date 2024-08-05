package com.ladbrokescoral.oxygen.betpackmp.configuration;

import static com.ladbrokescoral.oxygen.betpackmp.util.DateUtils.scrub;

import com.ladbrokescoral.oxygen.betpackmp.service.CmsService;
import com.ladbrokescoral.oxygen.betpackmp.service.CmsServiceImpl;
import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import io.netty.handler.timeout.WriteTimeoutHandler;
import java.util.concurrent.TimeUnit;
import java.util.function.UnaryOperator;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.DependsOn;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.http.client.reactive.ReactorResourceFactory;
import org.springframework.web.reactive.function.client.ClientRequest;
import org.springframework.web.reactive.function.client.ExchangeFilterFunction;
import org.springframework.web.reactive.function.client.ExchangeStrategies;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.netty.http.client.HttpClient;
import reactor.netty.resources.ConnectionProvider;

@Configuration
public class CmsApiConfig {
  public static final int BYTE_COUNT = 419430;
  public static final int POOL_SIZE = 1000;

  @Value("${cms.base.url}")
  private String cmsUrl;

  @Value("${cms.brand}")
  private String cmsBrand;

  @Value("${cms.connect.timeout}")
  private int connectTimeout;

  @Value("${cms.read.timeout}")
  private int readTimeout;

  @Value("${cms.write.timeout}")
  private int writeTimeout;

  @Value("${cms.retry.number}")
  private int retryNumber;

  @Value("${cms.retry.timeout}")
  private int retryTimeoutMillis;

  @Value("${cms.pool.size}")
  private int poolSize = POOL_SIZE;

  @Value("${cms.pool.use.epoll:false}")
  private boolean useEpoll;

  @Value("${cms.http.threads:50}")
  private int numberOfThreads;

  @Value("${cms.pool.keep.alive:false}")
  private boolean useKeepAlive;

  private WebClient cmsWebClient;

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Bean
  public WebClient cmsWebClient() {
    ReactorResourceFactory factory = new ReactorResourceFactory();
    ConnectionProvider provider = ConnectionProvider.create("cmsPool", poolSize);
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
                .runOn(EventLoopConfigure.getEventLoopGroup(useEpoll, "cms", numberOfThreads))
                .doOnConnected(
                    conn ->
                        conn.addHandlerLast(
                                new ReadTimeoutHandler(readTimeout, TimeUnit.MILLISECONDS))
                            .addHandlerLast(
                                new WriteTimeoutHandler(writeTimeout, TimeUnit.MILLISECONDS)));
    cmsWebClient =
        WebClient.builder()
            .baseUrl(cmsUrl)
            .filter(logRequest())
            .clientConnector(new ReactorClientHttpConnector(factory, mapper))
            .defaultHeader("Content-Type", "application/json")
            .exchangeStrategies(
                ExchangeStrategies.builder()
                    .codecs(configurer -> configurer.defaultCodecs().maxInMemorySize(BYTE_COUNT))
                    .build())
            .build();
    return cmsWebClient;
  }

  @Bean
  @DependsOn("cmsWebClient")
  public CmsService cmsService() {
    return new CmsServiceImpl(cmsWebClient);
  }

  private static ExchangeFilterFunction logRequest() {
    return ExchangeFilterFunction.ofRequestProcessor(
        (ClientRequest clientRequest) -> {
          ASYNC_LOGGER.info(
              "Request: {} {}",
              scrub(clientRequest.method().toString()),
              scrub(clientRequest.url().toString()));
          clientRequest
              .headers()
              .forEach(
                  (name, values) ->
                      values.forEach(
                          value -> ASYNC_LOGGER.info("{}={}", scrub(name), scrub(value))));
          return Mono.just(clientRequest);
        });
  }
}
