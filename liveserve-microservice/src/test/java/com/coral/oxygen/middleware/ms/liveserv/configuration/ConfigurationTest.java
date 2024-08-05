package com.coral.oxygen.middleware.ms.liveserv.configuration;

import com.coral.siteserver.api.SiteServerService;
import com.google.gson.Gson;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
class ConfigurationTest {
  Configuration config = new Configuration();

  @Test
  void testGsonObject() {

    Gson gson = config.gson();
    Assert.assertNotNull(gson);
  }

  @Test
  void testdistributedPrefix() {
    String prefix = "LOCAL";
    String result = config.distributedPrefix(prefix);
    Assert.assertNotNull(result);
  }

  @Test
  void testgetSiteServerService() {
    String baseUrl = "https://localhost:9090";
    String apiVersion = "2.54";
    String level = "BASIC";
    int connectionTimeout = 6;
    int readTimeout = 5;
    int retriesNumber = 2;
    SiteServerService ss =
        config.getSiteServerService(
            baseUrl, apiVersion, level, connectionTimeout, readTimeout, retriesNumber);
    Assert.assertNotNull(ss);
  }

  @Test
  void testgetSiteServerServiceException() {
    String baseUrl = "https://localhost:9090";
    String apiVersion = "2.54";
    String level = "BASIC";
    int connectionTimeout = 6;
    int readTimeout = 5;
    int retriesNumber = 2;

    SiteServerService ss =
        config.getSiteServerService(
            baseUrl, apiVersion, level, connectionTimeout, readTimeout, retriesNumber);
    Assert.assertNotNull(ss);
  }
}
