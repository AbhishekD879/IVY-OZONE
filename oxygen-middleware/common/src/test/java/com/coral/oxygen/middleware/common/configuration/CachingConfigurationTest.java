package com.coral.oxygen.middleware.common.configuration;

import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(MockitoJUnitRunner.class)
public class CachingConfigurationTest {

  @Test
  public void CachingConfig() {

    CachingConfiguration cachingConfiguration = new CachingConfiguration();
    ReflectionTestUtils.setField(cachingConfiguration, "virtualSportCacheTTL", 10L);
    ReflectionTestUtils.setField(cachingConfiguration, "timeUnit", "SECONDS");
    cachingConfiguration.cacheManager();
    Assert.assertEquals(
        10L, ReflectionTestUtils.getField(cachingConfiguration, "virtualSportCacheTTL"));
    Assert.assertEquals("SECONDS", ReflectionTestUtils.getField(cachingConfiguration, "timeUnit"));
  }
}
