package com.ladbrokescoral.cashout.config;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.coral.bpp.api.service.BppApiAsync;
import com.coral.bpp.api.service.impl.BppApiAsyncImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class BppConfigProxyTest {

  private BppApiConfigHeavy bppApiConfigHeavy;

  private BppApiConfigLight bppApiConfigLight;

  private BppApiAsync bppApiAsync;

  private static final String HOST = "localhost";

  private static final String PORT = "8888";

  @BeforeEach
  public void setUp() {
    bppApiConfigHeavy = new BppApiConfigHeavy();
    bppApiConfigLight = new BppApiConfigLight();
  }

  @Test
  void testBppHeavyWithProxy() {
    System.setProperty("http.proxyHost", HOST);
    System.setProperty("http.proxyPort", PORT);
    bppApiConfigHeavy.setCashoutHostAddress("localhost");
    bppApiConfigHeavy.setPoolSize(1000);
    bppApiConfigHeavy.setMaxIdleTime(20);
    bppApiConfigHeavy.setMaxLifeTime(60);
    bppApiConfigHeavy.setPendingAcquireTimeout(60);
    bppApiConfigHeavy.setEvictInBackground(120);
    bppApiAsync = bppApiConfigHeavy.bppApiAsyncHeavy();
    assertNotNull(bppApiAsync);
    assertTrue(bppApiAsync instanceof BppApiAsyncImpl);
  }

  @Test
  void testBppHeavyWithoutProxy() {
    bppApiConfigHeavy.setPoolSize(1000);
    bppApiConfigHeavy.setCashoutHostAddress("localhost");
    bppApiConfigHeavy.setMaxIdleTime(20);
    bppApiConfigHeavy.setMaxLifeTime(60);
    bppApiConfigHeavy.setPendingAcquireTimeout(60);
    bppApiConfigHeavy.setEvictInBackground(120);
    bppApiAsync = bppApiConfigHeavy.bppApiAsyncHeavy();
    assertNotNull(bppApiAsync);
    assertTrue(bppApiAsync instanceof BppApiAsyncImpl);
  }

  @Test
  void testBppLightWithProxy() {
    System.setProperty("http.proxyHost", HOST);
    System.setProperty("http.proxyPort", PORT);
    bppApiAsync = bppApiConfigLight.bppApiAsyncLight();
    assertNotNull(bppApiAsync);
    assertTrue(bppApiAsync instanceof BppApiAsyncImpl);
  }

  @Test
  void testBppLightWithoutProxy() {
    bppApiAsync = bppApiConfigLight.bppApiAsyncLight();
    assertNotNull(bppApiAsync);
    assertTrue(bppApiAsync instanceof BppApiAsyncImpl);
  }

  @Test
  void testEventLoopWithMoreThreads() {
    bppApiConfigHeavy.setCashoutHostAddress("localhost");
    bppApiConfigHeavy.setMaxIdleTime(20);
    bppApiConfigHeavy.setMaxLifeTime(60);
    bppApiConfigHeavy.setPendingAcquireTimeout(60);
    bppApiConfigHeavy.setEvictInBackground(120);
    bppApiConfigHeavy.setNumberOfThreads(100);
    bppApiConfigHeavy.setPoolSize(1000);
    bppApiAsync = bppApiConfigHeavy.bppApiAsyncHeavy();
    assertNotNull(bppApiAsync);
  }
}
