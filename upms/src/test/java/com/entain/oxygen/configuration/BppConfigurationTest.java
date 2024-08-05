package com.entain.oxygen.configuration;

import com.coral.bpp.api.service.BppApiAsync;
import com.coral.bpp.api.service.impl.BppApiAsyncImpl;
import com.entain.oxygen.bpp.BppConfigLightProps;
import com.entain.oxygen.bpp.BppConfiguration;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class BppConfigurationTest {

  private static final String BPP_URL = "http://bpp.internal.tst.coral.co.uk";

  private static final String HOST = "localhost";

  private static final String PORT = "8888";

  @Mock private BppConfigLightProps bppConfigLightProps;

  private BppApiAsync bppApiAsync;

  private BppConfiguration bppConfiguration;

  @BeforeEach
  public void init() {
    int poolSize = 100;
    Mockito.when(bppConfigLightProps.getPoolSize()).thenReturn(poolSize);
    bppConfiguration = new BppConfiguration(BPP_URL, bppConfigLightProps);
  }

  @Test
  void testBppAsyncLightWithProxy() {

    System.setProperty("http.proxyHost", HOST);
    System.setProperty("http.proxyPort", PORT);
    bppApiAsync = bppConfiguration.bppApiAsyncLight();
    Assertions.assertNotNull(bppApiAsync);
    Assertions.assertTrue(bppApiAsync instanceof BppApiAsyncImpl);
  }

  @Test
  void testBppAsyncLightWithoutProxy() {
    bppApiAsync = bppConfiguration.bppApiAsyncLight();
    Assertions.assertNotNull(bppApiAsync);
    Assertions.assertTrue(bppApiAsync instanceof BppApiAsyncImpl);
  }

  @Test
  void testEventLoopWithMoreThreads() {
    Mockito.when(bppConfigLightProps.getThreads()).thenReturn(100);
    bppApiAsync = bppConfiguration.bppApiAsyncLight();
    Assertions.assertNotNull(bppApiAsync);
    Assertions.assertTrue(bppApiAsync instanceof BppApiAsyncImpl);
  }
}
