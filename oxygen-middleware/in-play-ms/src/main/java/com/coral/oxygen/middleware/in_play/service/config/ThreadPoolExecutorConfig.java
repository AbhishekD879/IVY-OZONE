package com.coral.oxygen.middleware.in_play.service.config;

import io.netty.util.NettyRuntime;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@Configuration
public class ThreadPoolExecutorConfig {

  private static final int KEEP_ALIVE_SECONDS = 3000;
  private static final int THREAD_COUNT = 2;

  @Bean("threadPoolTaskExecutor")
  public ThreadPoolTaskExecutor threadPoolTaskExecutor() {
    int threads = NettyRuntime.availableProcessors() * THREAD_COUNT;
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setThreadNamePrefix("TH");
    executor.setKeepAliveSeconds(KEEP_ALIVE_SECONDS);
    executor.setDaemon(false);
    executor.setCorePoolSize(threads);
    executor.setMaxPoolSize(threads);
    executor.setThreadPriority(Thread.MAX_PRIORITY);
    executor.setAllowCoreThreadTimeOut(true);
    executor.afterPropertiesSet();

    return executor;
  }
}
