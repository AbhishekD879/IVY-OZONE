package com.ladbrokescoral.aggregation.config;

import static org.junit.jupiter.api.Assertions.assertNotNull;

import org.junit.jupiter.api.Test;
import org.springframework.web.reactive.function.client.WebClient;

public class SilksProviderWebClientTest extends BaseProxyTest {

  @Test
  public void testSilkWebClientWithProxyWithNewConnection() {
    System.setProperty("http.proxyHost", HOST);
    System.setProperty("http.proxyPort", PORT);
    WebClient webClient = getWebClientConfig().providerWebClientForSilks(WebClient.builder(), 0);
    assertNotNull(webClient);
  }

  @Test
  public void testSilkWebClientWithProxyWithConnectionPool() {
    getWebClientConfig().setUsePool(true);
    System.setProperty("http.proxyHost", HOST);
    System.setProperty("http.proxyPort", PORT);
    WebClient webClient = getWebClientConfig().providerWebClientForSilks(WebClient.builder(), 0);
    assertNotNull(webClient);
  }

  @Test
  public void testSilksWebClientWithoutProxy() {
    WebClient webClient = getWebClientConfig().providerWebClientForSilks(WebClient.builder(), 0);
    assertNotNull(webClient);
  }
}
