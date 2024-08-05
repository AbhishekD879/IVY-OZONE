package com.entain.oxygen.betbuilder_middleware.config;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;

@ExtendWith(SpringExtension.class)
@Import(PricingGatewayClientProperties.class)
class PricingGatewayWebClientConfigTest {
  private PricingGatewayWebClientConfig pricingGatewayWebClientConfig;

  @Autowired PricingGatewayClientProperties pricingGatewayClientProperties;

  @MockBean(name = "pricingGatewayWebClient")
  private WebClient pricingGatewayWebClient;

  @MockBean(name = "pricingGatewayHttpClient")
  private HttpClient pricingGatewayHttpClient;

  private EventLoopConfigurer eventLoopConfigurer;

  @BeforeEach
  public void init() {
    pricingGatewayClientProperties.setMaxConnections(10);
    pricingGatewayClientProperties.setBaseUrl("http://bpg.dev.env.works/api/");
    pricingGatewayClientProperties.setKeepAlive(true);
    pricingGatewayClientProperties.setReadTimeoutMillis(5000);
    pricingGatewayClientProperties.setMaxInMemorySize(2097152);
    pricingGatewayClientProperties.setConnectionTimeoutMillis(5000);
    pricingGatewayClientProperties.setUseEpoll(false);
    pricingGatewayClientProperties.setWriteTimeoutMillis(5000);
    pricingGatewayClientProperties.setThreadNamePrefix("PRICING-GATEWAY-LOOP");
    pricingGatewayClientProperties.setNumberOfThreads(10);
    pricingGatewayClientProperties.setConnectionName("PricingGateway-CONNECTIONS");
    pricingGatewayClientProperties.setContentType("application/json");
    pricingGatewayClientProperties.setPendingAcquireMaxCount(1000);
    pricingGatewayClientProperties.setPendingAcquireTimeout(120);
    pricingGatewayClientProperties.setMaxIdleTime(20);
    pricingGatewayClientProperties.setMaxLifeTime(60);
    pricingGatewayClientProperties.setEvictInBackground(120);
    pricingGatewayClientProperties.setThreadMultiplier(2);
    pricingGatewayClientProperties.setThreadKeepAliveSeconds(120);
    pricingGatewayClientProperties.setTcpKeepIdle(300);
    pricingGatewayClientProperties.setTcpKeepInterval(60);
    pricingGatewayClientProperties.setTcpKeepCount(8);

    pricingGatewayWebClientConfig =
        new PricingGatewayWebClientConfig(pricingGatewayClientProperties);
  }

  @Test
  void testPricingGatewayWebClient() {
    Assertions.assertDoesNotThrow(
        () ->
            pricingGatewayWebClientConfig.pricingGatewayWebClient(
                pricingGatewayHttpClient, pricingGatewayClientProperties));
  }

  @Test
  void testPricingGatewayHttpClient() {
    Assertions.assertDoesNotThrow(() -> pricingGatewayWebClientConfig.pricingGatewayHttpClient());
  }

  @Test
  void testHttpclientWithEpollTrue() {
    String os = System.getProperty("os.name");
    pricingGatewayClientProperties.setUseEpoll(os.contains("Windows") ? false : true);
    Assertions.assertDoesNotThrow(() -> pricingGatewayWebClientConfig.pricingGatewayHttpClient());
  }

  @Test
  void testHttpclientWithZeroThreads() {
    pricingGatewayClientProperties.setNumberOfThreads(0);
    Assertions.assertDoesNotThrow(() -> pricingGatewayWebClientConfig.pricingGatewayHttpClient());
  }
}
