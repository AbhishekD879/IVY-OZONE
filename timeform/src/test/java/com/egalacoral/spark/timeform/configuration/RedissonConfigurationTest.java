package com.egalacoral.spark.timeform.configuration;

import java.util.List;
import org.junit.Assert;
import org.junit.Test;

public class RedissonConfigurationTest {

  private RedissonConfiguration redissonConfiguration = new RedissonConfiguration();

  @Test
  public void testSentinelPath() {
    String path =
        "timeform-dev1-0001-001.vegjyb.0001.euw1.cache.amazonaws.com:6379, timeform-dev1-0001-002.vegjyb.0001.euw1.cache.amazonaws.com:6379, timeform-dev1-0001-003.vegjyb.0001.euw1.cache.amazonaws.com:6379";

    List<String> sentinelAddresses = redissonConfiguration.createSentinelNodeAddress(path);
    Assert.assertEquals(
        "[redis://timeform-dev1-0001-001.vegjyb.0001.euw1.cache.amazonaws.com:6379, redis://timeform-dev1-0001-002.vegjyb.0001.euw1.cache.amazonaws.com:6379, redis://timeform-dev1-0001-003.vegjyb.0001.euw1.cache.amazonaws.com:6379]",
        sentinelAddresses.toString());
  }
}
