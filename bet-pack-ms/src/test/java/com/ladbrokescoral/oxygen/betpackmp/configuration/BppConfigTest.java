package com.ladbrokescoral.oxygen.betpackmp.configuration;

import com.coral.bpp.api.service.BppApiAsync;
import java.lang.reflect.Field;
import org.assertj.core.api.Assertions;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class BppConfigTest implements WithAssertions {

  @InjectMocks private BppConfig bppConfig;

  @BeforeAll
  void init() throws Exception {
    bppConfig = new BppConfig();
    Field url = BppConfig.class.getDeclaredField("url");
    Field retryNumber = BppConfig.class.getDeclaredField("retryNumber");
    Field connectTimeout = BppConfig.class.getDeclaredField("connectTimeout");
    Field readTimeout = BppConfig.class.getDeclaredField("readTimeout");
    Field writeTimeout = BppConfig.class.getDeclaredField("writeTimeout");
    Field retryTimeoutMillis = BppConfig.class.getDeclaredField("retryTimeoutMillis");
    Field poolSize = BppConfig.class.getDeclaredField("poolSize");
    Field poolTimeout = BppConfig.class.getDeclaredField("poolTimeout");
    Field useEpoll = BppConfig.class.getDeclaredField("useEpoll");
    Field numberOfThreads = BppConfig.class.getDeclaredField("numberOfThreads");
    Field useKeepAlive = BppConfig.class.getDeclaredField("useKeepAlive");
    url.setAccessible(true);
    url.set(bppConfig, "http://localhost:9090/Proxy");
    retryNumber.setAccessible(true);
    retryNumber.set(bppConfig, 3);
    connectTimeout.setAccessible(true);
    connectTimeout.set(bppConfig, 2000);
    readTimeout.setAccessible(true);
    readTimeout.set(bppConfig, 3000);
    writeTimeout.setAccessible(true);
    writeTimeout.set(bppConfig, 2000);
    retryTimeoutMillis.setAccessible(true);
    retryTimeoutMillis.set(bppConfig, 0);
    poolSize.setAccessible(true);
    poolSize.set(bppConfig, 2000);
    poolTimeout.setAccessible(true);
    poolTimeout.set(bppConfig, 30000);
    useEpoll.setAccessible(true);
    useEpoll.set(bppConfig, false);
    numberOfThreads.setAccessible(true);
    numberOfThreads.set(bppConfig, 50);
    useKeepAlive.setAccessible(true);
    useKeepAlive.set(bppConfig, false);
  }

  @Test
  void bppApiAsyncTest() {
    BppApiAsync bppApiAsync = bppConfig.bppApiAsync();
    Assertions.assertThat(bppApiAsync).isNotNull();
  }

  @Test
  void bppApiAsyncKeepAliveTrueTest() throws NoSuchFieldException, IllegalAccessException {
    Field useEpoll = BppConfig.class.getDeclaredField("useEpoll");
    useEpoll.setAccessible(true);
    useEpoll.set(bppConfig, false);
    Field useKeepAlive = BppConfig.class.getDeclaredField("useKeepAlive");
    useKeepAlive.setAccessible(true);
    useKeepAlive.set(bppConfig, true);
    BppApiAsync bppApiAsync = bppConfig.bppApiAsync();
    Assertions.assertThat(bppApiAsync).isNotNull();
  }
}
