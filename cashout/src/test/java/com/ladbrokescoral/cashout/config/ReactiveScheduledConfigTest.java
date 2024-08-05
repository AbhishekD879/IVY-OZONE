package com.ladbrokescoral.cashout.config;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

class ReactiveScheduledConfigTest {

  private ReactiveSchedulerConfig reactiveSchedulerConfig;

  @BeforeEach
  public void init() {
    reactiveSchedulerConfig = new ReactiveSchedulerConfig();
  }

  @Test
  void testThreadPoolExecutorTest() {
    ThreadPoolTaskExecutor threadPoolTaskExecutor = null;
    threadPoolTaskExecutor = reactiveSchedulerConfig.threadPoolTaskExecutor(10, 50, 0);
    assertNotNull(threadPoolTaskExecutor);
    assertEquals(10, threadPoolTaskExecutor.getCorePoolSize());
    assertEquals(50, threadPoolTaskExecutor.getMaxPoolSize());
  }
}
