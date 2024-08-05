package com.coral.oxygen.middleware.common.service;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.when;

import com.amazonaws.auth.AWSCredentialsProvider;
import com.coral.oxygen.middleware.common.configuration.cfcache.BrandCacheService;
import com.coral.oxygen.middleware.common.configuration.cfcache.BrandCacheServiceProviderImpl;
import com.coral.oxygen.middleware.common.configuration.cfcache.CloudFlareClient;
import com.coral.oxygen.middleware.common.configuration.cfcache.S3BrandProperties;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
public class BrandCacheServiceProviderTest {
  @Mock CloudFlareClient cloudFlareClient;
  S3BrandProperties properties = new S3BrandProperties();
  @Mock S3BrandProperties.S3BrandConfig config;
  BrandCacheServiceProviderImpl brandCacheServiceProviderImpl;
  @Mock AWSCredentialsProvider awsS3CredentialsProvider;

  @Before
  public void init() {
    when(config.getPurgeZoneId()).thenReturn("ZoneId");
    when(config.getBasePath()).thenReturn("/home/base");
    when(config.getRegion()).thenReturn("india");
    when(config.isEnabled()).thenReturn(true);
    when(config.getPurgeZoneId()).thenReturn("PurgeZoneId");
    when(config.getPurgeUrl()).thenReturn(new String[] {"http://purge"});
    Map<String, S3BrandProperties.S3BrandConfig> configs = new HashMap<>();
    configs.put("Bma", config);
    properties.setConfigs(configs);
    brandCacheServiceProviderImpl =
        new BrandCacheServiceProviderImpl(
            properties, cloudFlareClient, 10, 0, 1, 10, awsS3CredentialsProvider);
  }

  @Test
  public void getCacheServiceTest() {
    List<BrandCacheService> services = brandCacheServiceProviderImpl.getCacheService("Bma");
    assertEquals(1, services.size());
  }

  @Test
  public void getCacheServiceTestWhenConfigFalse() {
    when(config.isEnabled()).thenReturn(false);

    brandCacheServiceProviderImpl =
        new BrandCacheServiceProviderImpl(
            properties, cloudFlareClient, 10, 0, 1, 10, awsS3CredentialsProvider);
    List<BrandCacheService> services = brandCacheServiceProviderImpl.getCacheService("Bma");
    assertEquals(0, services.size());
  }

  @After
  public void tearDown() {
    brandCacheServiceProviderImpl.shutdown();
  }
}
