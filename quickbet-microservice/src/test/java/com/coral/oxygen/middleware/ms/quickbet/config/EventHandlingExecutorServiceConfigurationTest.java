package com.coral.oxygen.middleware.ms.quickbet.config;

import com.coral.oxygen.middleware.ms.quickbet.configuration.EventHandlingExecutorServiceConfiguration;
import java.lang.reflect.Field;
import java.util.concurrent.Executor;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.scheduling.concurrent.ThreadPoolTaskScheduler;

class EventHandlingExecutorServiceConfigurationTest {

  private EventHandlingExecutorServiceConfiguration configuration;

  @BeforeEach
  public void init() throws NoSuchFieldException, IllegalAccessException {
    configuration = new EventHandlingExecutorServiceConfiguration();
    Field numOfThreadsForEventHandling =
        EventHandlingExecutorServiceConfiguration.class.getDeclaredField(
            "numOfThreadsForEventHandling");
    numOfThreadsForEventHandling.setAccessible(true);
    numOfThreadsForEventHandling.set(configuration, 100);
    Field corePoolSize =
        EventHandlingExecutorServiceConfiguration.class.getDeclaredField("corePoolSize");
    corePoolSize.setAccessible(true);
    corePoolSize.set(configuration, 10);
    Field queueCapacity =
        EventHandlingExecutorServiceConfiguration.class.getDeclaredField("queueCapacity");
    queueCapacity.setAccessible(true);
    queueCapacity.set(configuration, 10);
    Field poolSize = EventHandlingExecutorServiceConfiguration.class.getDeclaredField("poolSize");
    poolSize.setAccessible(true);
    poolSize.set(configuration, 5);
  }

  @Test
  void testExecutor() {

    Executor executor = configuration.eventHandlingExecutorService();
    Assertions.assertNotNull(executor);
    Assertions.assertEquals(10, ((ThreadPoolTaskExecutor) executor).getCorePoolSize());
    Assertions.assertEquals(100, ((ThreadPoolTaskExecutor) executor).getMaxPoolSize());
  }

  @Test
  void testExecutorWithNegativeQueueCapacity() throws NoSuchFieldException, IllegalAccessException {
    Field queueCapacity =
        EventHandlingExecutorServiceConfiguration.class.getDeclaredField("queueCapacity");
    queueCapacity.setAccessible(true);
    queueCapacity.set(configuration, -1);
    Executor executor = configuration.eventHandlingExecutorService();
    Assertions.assertNotNull(executor);
    Assertions.assertEquals(10, ((ThreadPoolTaskExecutor) executor).getCorePoolSize());
    Assertions.assertEquals(100, ((ThreadPoolTaskExecutor) executor).getMaxPoolSize());
  }

  @Test
  void testThreadPoolTaskScheduler() {

    ThreadPoolTaskScheduler scheduler = configuration.threadPoolTaskScheduler();
    Assertions.assertNotNull(scheduler);
    Assertions.assertEquals("ThreadPoolTaskScheduler", scheduler.getThreadNamePrefix());
  }
}
