package com.ladbrokescoral.aggregation.config;

import static org.junit.jupiter.api.Assertions.assertNotNull;

import org.junit.jupiter.api.Test;
import org.springframework.web.reactive.function.client.WebClient;

public class ImageProviderWebClientTest extends BaseProxyTest {
  @Test
  public void testImagesWebClientWithProxyWithNewConnection() {

    System.setProperty("http.proxyHost", HOST);
    System.setProperty("http.proxyPort", PORT);
    WebClient webClient = getWebClientConfig().providerWebClientForImages(WebClient.builder(), 0);
    assertNotNull(webClient);
  }

  @Test
  public void testImagesWebClientWithProxyWithConnectionPool() {
    getWebClientConfig().setUsePool(true);
    System.setProperty("http.proxyHost", HOST);
    System.setProperty("http.proxyPort", PORT);
    WebClient webClient = getWebClientConfig().providerWebClientForImages(WebClient.builder(), 0);
    assertNotNull(webClient);
  }

  @Test
  public void testImagesWebClientWithoutProxy() {
    WebClient webClient = getWebClientConfig().providerWebClientForImages(WebClient.builder(), 0);
    assertNotNull(webClient);
  }

  @Test
  public void testEventLoopConfigurerWithMaximumThreads() {
    WebClient webClient = getWebClientConfig().providerWebClientForImages(WebClient.builder(), 10);
    assertNotNull(webClient);
  }
}
