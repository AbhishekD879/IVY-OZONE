package com.coral.oxygen.middleware.ms.quickbet.config;

import com.coral.oxygen.middleware.ms.quickbet.configuration.SiteServerApiConfiguration;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.cache.CacheManager;

class SiteServApiConfigurationTest {

  private SiteServerApiConfiguration siteServerApiConfiguration;

  @BeforeEach
  public void init() {

    siteServerApiConfiguration = new SiteServerApiConfiguration();
  }

  @Test
  void testSiteServ() throws KeyManagementException, NoSuchAlgorithmException {
    SiteServerApi siteServerApi = null;
    siteServerApi =
        siteServerApiConfiguration.siteServerAPI(
            "https://ss-tst2.coral.co.uk/",
            3,
            3,
            3,
            SiteServerApi.Level.BASIC.name(),
            2,
            300,
            "2.54",
            "2.65",
            false);
    Assertions.assertNotNull(siteServerApi);
  }

  @Test
  void testSiteServPriceBoostEnabled() throws KeyManagementException, NoSuchAlgorithmException {
    SiteServerApi siteServerApi = null;
    siteServerApi =
        siteServerApiConfiguration.siteServerAPI(
            "https://ss-tst2.coral.co.uk/",
            3,
            3,
            3,
            SiteServerApi.Level.BASIC.name(),
            2,
            300,
            "2.54",
            "2.65",
            true);
    Assertions.assertNotNull(siteServerApi);
  }

  @Test
  void testCacheManager() {
    CacheManager cacheManager = null;
    cacheManager = siteServerApiConfiguration.cacheManager(2, 2, "outcomes");
    Assertions.assertNotNull(cacheManager);
  }

  @Test
  void testNoCacheManager() {
    CacheManager cacheManager = null;
    cacheManager = siteServerApiConfiguration.noOpCacheManager();
    Assertions.assertNotNull(cacheManager);
  }
}
