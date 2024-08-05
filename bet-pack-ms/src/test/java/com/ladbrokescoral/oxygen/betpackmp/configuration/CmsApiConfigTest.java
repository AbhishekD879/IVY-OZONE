package com.ladbrokescoral.oxygen.betpackmp.configuration;

import com.ladbrokescoral.oxygen.betpackmp.service.CmsService;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.reactive.function.client.WebClient;

@ExtendWith(MockitoExtension.class)
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class CmsApiConfigTest implements WithAssertions {

  @InjectMocks private CmsApiConfig cmsApiConfig;

  @BeforeAll
  void init() {
    cmsApiConfig = new CmsApiConfig();
    ReflectionTestUtils.setField(cmsApiConfig, "cmsUrl", "http://localhost:8083");
    ReflectionTestUtils.setField(cmsApiConfig, "cmsBrand", "bma");
    ReflectionTestUtils.setField(cmsApiConfig, "connectTimeout", 2000);
    ReflectionTestUtils.setField(cmsApiConfig, "readTimeout", 3000);
    ReflectionTestUtils.setField(cmsApiConfig, "writeTimeout", 2000);
    ReflectionTestUtils.setField(cmsApiConfig, "retryNumber", 0);
    ReflectionTestUtils.setField(cmsApiConfig, "retryTimeoutMillis", 0);
    ReflectionTestUtils.setField(cmsApiConfig, "poolSize", 100);
    ReflectionTestUtils.setField(cmsApiConfig, "useEpoll", true);
    ReflectionTestUtils.setField(cmsApiConfig, "numberOfThreads", 50);
    ReflectionTestUtils.setField(cmsApiConfig, "useKeepAlive", true);
  }

  @Test
  void cmsWebClient() {
    WebClient webClient = cmsApiConfig.cmsWebClient();
    Assertions.assertNotNull(webClient);
  }

  @Test
  void cmsWebClientUseEpollFalse() {
    ReflectionTestUtils.setField(cmsApiConfig, "useEpoll", false);
    ReflectionTestUtils.setField(cmsApiConfig, "useKeepAlive", false);
    WebClient webClient = cmsApiConfig.cmsWebClient();
    Assertions.assertNotNull(webClient);
  }

  @Test
  void cmsService() {
    cmsApiConfig = new CmsApiConfig();
    CmsService result = cmsApiConfig.cmsService();
    Assertions.assertNotNull(result);
  }
}
