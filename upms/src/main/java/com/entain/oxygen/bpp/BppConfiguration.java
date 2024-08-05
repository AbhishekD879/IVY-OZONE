package com.entain.oxygen.bpp;

import com.coral.bpp.api.service.BppApiAsync;
import com.coral.bpp.api.service.impl.BppApiAsyncImpl;
import com.entain.oxygen.configuration.EventLoopConfigurer;
import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import io.netty.handler.timeout.WriteTimeoutHandler;
import java.util.concurrent.TimeUnit;
import java.util.function.UnaryOperator;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.http.client.reactive.ReactorResourceFactory;
import reactor.netty.http.client.HttpClient;
import reactor.netty.resources.ConnectionProvider;

@Configuration
@EnableConfigurationProperties
public class BppConfiguration {

  private final String bppUrl;

  private final BppConfigLightProps bppConfigLightProps;

  @Autowired
  public BppConfiguration(
      @Value("${bpp.api.url}") String bppUrl, BppConfigLightProps bppConfigLightProps) {
    this.bppUrl = bppUrl;
    this.bppConfigLightProps = bppConfigLightProps;
  }

  @Bean
  public BppApiAsync bppApiAsyncLight() {
    return bppApiAsync("bpp-light-pool", "bpp-Light", bppConfigLightProps);
  }

  private BppApiAsync bppApiAsync(String poolName, String threadPrefix, BppProperties properties) {
    ReactorResourceFactory factory = new ReactorResourceFactory();
    ConnectionProvider provider = ConnectionProvider.create(poolName, properties.getPoolSize());
    factory.setUseGlobalResources(false);
    factory.setConnectionProvider(provider);
    factory.afterPropertiesSet();

    UnaryOperator<HttpClient> mapper =
        client ->
            HttpClient.create(provider)
                .proxyWithSystemProperties()
                .compress(true)
                .keepAlive(properties.isKeepAlive())
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, properties.getConnectTimeout())
                .option(ChannelOption.SO_KEEPALIVE, properties.isKeepAlive())
                .runOn(EventLoopConfigurer.getEventLoopGroup(threadPrefix, properties.getThreads()))
                .doOnConnected(
                    conn ->
                        conn.addHandlerLast(
                                new ReadTimeoutHandler(
                                    properties.getReadTimeout(), TimeUnit.MILLISECONDS))
                            .addHandlerLast(
                                new WriteTimeoutHandler(
                                    properties.getWriteTimeout(), TimeUnit.MILLISECONDS)));

    return new BppApiAsyncImpl(
        bppUrl,
        properties.getRetryNumber(),
        properties.getRetryTimeout(),
        new ReactorClientHttpConnector(factory, mapper));
  }
}
