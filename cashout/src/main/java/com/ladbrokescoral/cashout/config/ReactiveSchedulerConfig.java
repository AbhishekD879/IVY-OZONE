package com.ladbrokescoral.cashout.config;

import java.util.concurrent.ThreadPoolExecutor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@Configuration
public class ReactiveSchedulerConfig {

  @Bean("threadPoolTaskExecutor")
  public ThreadPoolTaskExecutor threadPoolTaskExecutor(
      @Value("${cashout.thread.pool.core.size:0}") int coreSize,
      @Value("${cashout.thread.pool.max.size:100}") int maxPoolSize,
      @Value("${cashout.thread.pool.queue.capacity:0}") int queueCapacity) {

    ThreadPoolTaskExecutor threadPoolTaskExecutor = new ThreadPoolTaskExecutor();
    threadPoolTaskExecutor.setCorePoolSize(coreSize);
    threadPoolTaskExecutor.setMaxPoolSize(maxPoolSize);
    threadPoolTaskExecutor.setWaitForTasksToCompleteOnShutdown(false);
    threadPoolTaskExecutor.setThreadGroupName("Cashout-TP-");
    threadPoolTaskExecutor.setAllowCoreThreadTimeOut(true);
    threadPoolTaskExecutor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
    threadPoolTaskExecutor.afterPropertiesSet();
    return threadPoolTaskExecutor;
  }
}
