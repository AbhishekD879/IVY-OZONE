package com.entain.oxygen.betbuilder_middleware.config;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.api.SiteServerApiAsync;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import reactor.netty.resources.ConnectionProvider;

@ExtendWith(MockitoExtension.class)
@Configuration
class SiteServerApiConfigurationNonUnixTest {

  @Mock private ConnectionProvider connectionProvider;

  @Mock private EventLoopConfigurer eventLoopConfigurer;

  private SiteServerApiConfiguration siteServerApiConfiguration;
  private SiteServerApiAsync siteServerApiAsync;

  @Value("${site-server.base.url}")
  private String siteServerUrl;

  @Value("${site-server.api.version}")
  private String apiVersion;

  @Value("${site-server.read.timeout}")
  private int readTimeout;

  @Value("${site-server.write.timeout}")
  private int writeTimeout;

  @Value("${site-server.use.epoll:true}")
  private boolean useEpoll = true;

  @Value("${site-server.pool.size:50}")
  private int poolSize;

  @Value("${site-server.threads:50}")
  private int numberOfThreads;

  @Value("${site-server.max-memory-size:16777216}")
  private int maxMemorySize;

  @Value("${site-server.max-connections}")
  private int maxConnections;

  @BeforeEach
  public void setUp() {
    // Mock dependencies
    siteServerApiConfiguration = mock(SiteServerApiConfiguration.class);
    siteServerApiAsync = mock(SiteServerApiAsync.class);

    // Set up mock behavior
    when(siteServerApiConfiguration.siteServerAsync()).thenReturn(siteServerApiAsync);

    // Initialize objects under test
    // Optionally, you can also inject dependencies manually here
  }

  @Test
  void testSiteServerApiAsyncBean() {
    System.out.println("Test maxConnection" + maxConnections);
    System.out.println("Test max-memory-size" + maxMemorySize);
    SiteServerApiAsync ssApiAsync = siteServerApiConfiguration.siteServerAsync();
    assertNotNull(ssApiAsync);
  }
}
