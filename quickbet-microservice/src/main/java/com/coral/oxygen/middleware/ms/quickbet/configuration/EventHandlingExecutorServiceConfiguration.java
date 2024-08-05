package com.coral.oxygen.middleware.ms.quickbet.configuration;

import java.util.concurrent.Executor;
import java.util.concurrent.ThreadPoolExecutor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.scheduling.concurrent.ThreadPoolTaskScheduler;

@Configuration
public class EventHandlingExecutorServiceConfiguration {

  @Value("${remote-betslip.event-handler.threads:200}")
  private int numOfThreadsForEventHandling;

  @Value("${remote-betslip.event-handler.core.pool.size:10}")
  private int corePoolSize;

  @Value("${remote-betslip.event-handler.queue.capacity:0}")
  private int queueCapacity;

  @Value("${remote-betslip.event-handler.scheduler.pool.size:0}")
  private int poolSize;

  @Bean
  public Executor eventHandlingExecutorService() {
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setCorePoolSize(corePoolSize);
    executor.setMaxPoolSize(numOfThreadsForEventHandling);
    if (queueCapacity != -1) executor.setQueueCapacity(queueCapacity);
    executor.setWaitForTasksToCompleteOnShutdown(true);
    executor.setThreadGroupName("Remote-Betslip-coral-TP-");
    executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
    executor.setAllowCoreThreadTimeOut(true);
    executor.afterPropertiesSet();
    executor.initialize();
    return executor;
  }

  @Bean
  public ThreadPoolTaskScheduler threadPoolTaskScheduler() {
    ThreadPoolTaskScheduler threadPoolTaskScheduler = new ThreadPoolTaskScheduler();
    threadPoolTaskScheduler.setPoolSize(poolSize);
    threadPoolTaskScheduler.setThreadNamePrefix("ThreadPoolTaskScheduler");
    threadPoolTaskScheduler.setWaitForTasksToCompleteOnShutdown(false);
    threadPoolTaskScheduler.afterPropertiesSet();
    return threadPoolTaskScheduler;
  }
}
