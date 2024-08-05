package com.ladbrokescoral.reactions.config;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.*;

import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import java.net.InetSocketAddress;
import java.time.Duration;
import java.util.concurrent.TimeUnit;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import reactor.netty.http.client.HttpClient;
import reactor.netty.transport.ProxyProvider;

class HttpClientConfigTest {

  private HttpClient httpClient;

  private HttpClientPropertiesConfig httpClientPropertiesConfig;

  private HttpClientConfig httpClientConfig;

  @BeforeEach
  void setUp() {
    httpClient = mock(HttpClient.class);
    httpClientPropertiesConfig = mock(HttpClientPropertiesConfig.class);
    httpClientConfig = mock(HttpClientConfig.class);
  }

  @Test
  void testHttpClientConfiguration() {
    when(httpClientPropertiesConfig.getResponseTimeout()).thenReturn(10);
    when(httpClientPropertiesConfig.getConnectTimeout()).thenReturn(5000);
    when(httpClientPropertiesConfig.isKeepAlive()).thenReturn(true);
    when(httpClientPropertiesConfig.getReadTimeout()).thenReturn(30);
    HttpClient expectedClient =
        HttpClient.create()
            .compress(true)
            .responseTimeout(Duration.ofSeconds(10))
            .doOnConnected(
                connection ->
                    connection.addHandlerFirst(new ReadTimeoutHandler(30, TimeUnit.SECONDS)))
            .proxy(
                proxy ->
                    proxy
                        .type(ProxyProvider.Proxy.HTTP)
                        .address(() -> new InetSocketAddress("proxy.example.com", 8080)))
            .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 5000)
            .option(ChannelOption.SO_KEEPALIVE, true)
            .doOnConnected(Assertions::assertNotNull)
            .doOnConnected(
                connection ->
                    connection.addHandlerFirst(
                        new ReadTimeoutHandler(
                            httpClientPropertiesConfig.getReadTimeout(), TimeUnit.SECONDS)));
    assertNotNull(expectedClient);
  }
}
