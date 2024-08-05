package com.ladbrokescoral.oxygen.configuration;

import java.util.concurrent.Executor;
import java.util.concurrent.ThreadPoolExecutor;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.repository.configuration.EnableRedisRepositories;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@Configuration
@EnableAsync
@EnableRedisRepositories(basePackages = {"com.ladbrokescoral.oxygen"})
public class ApplicationConfiguration {

  @Value("${leaderboard.threadpool.core-size:5}")
  private int coreThreadPoolSize;

  @Value("${leaderboard.threadpool.max-size:20}")
  private int maxThreadPoolSize;

  @Value("${leaderboard.threadpool.queue.capacity:0}")
  private int queueCapacity;

  @Bean
  public Executor asyncExecutor() {
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setMaxPoolSize(Runtime.getRuntime().availableProcessors());
    executor.initialize();
    return executor;
  }

  @Bean
  @Qualifier("distributedPrefix")
  public String distributedPrefix(@Value("${distributed.prefix}") String prefix) {
    return prefix;
  }

  @Bean(name = "leaderboardExecutor")
  public ThreadPoolTaskExecutor taskExecutor() {
    ThreadPoolTaskExecutor taskExecutor = new ThreadPoolTaskExecutor();
    taskExecutor.setCorePoolSize(coreThreadPoolSize);
    taskExecutor.setMaxPoolSize(maxThreadPoolSize);
    if (queueCapacity != -1) taskExecutor.setQueueCapacity(queueCapacity);
    taskExecutor.setQueueCapacity(queueCapacity);
    taskExecutor.setAllowCoreThreadTimeOut(true);
    taskExecutor.setThreadGroupName("LDRBRD");
    taskExecutor.setThreadNamePrefix("LEADERBOARD-");
    taskExecutor.setDaemon(false);
    taskExecutor.setWaitForTasksToCompleteOnShutdown(true);
    taskExecutor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
    taskExecutor.afterPropertiesSet();
    taskExecutor.initialize();
    return taskExecutor;
  }
}
