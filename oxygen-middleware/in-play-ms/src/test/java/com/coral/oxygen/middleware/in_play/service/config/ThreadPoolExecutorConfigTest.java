package com.coral.oxygen.middleware.in_play.service.config;

import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
public class ThreadPoolExecutorConfigTest {

  @Test
  public void ThreadPoolConfigTest() {
    ThreadPoolExecutorConfig threadPoolExecutorConfig = new ThreadPoolExecutorConfig();
    threadPoolExecutorConfig.threadPoolTaskExecutor();
    Assert.assertNotNull(threadPoolExecutorConfig);
  }
}
