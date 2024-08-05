package com.entain.oxygen.betbuilder_middleware.config;

import io.netty.channel.EventLoopGroup;
import io.netty.channel.epoll.EpollEventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.util.NettyRuntime;
import java.util.concurrent.Executor;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

public class EventLoopConfigurer {

  private EventLoopConfigurer() {}

  public static EventLoopGroup getEventLoopGroup(
      boolean useEpoll,
      String threadNamePrefix,
      int numberOfThreads,
      int threadMultiplier,
      int threadKeepAliveSeconds) {

    int threads = NettyRuntime.availableProcessors() * threadMultiplier;
    if (numberOfThreads != 0) threads = numberOfThreads;
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setThreadNamePrefix(threadNamePrefix);
    executor.setKeepAliveSeconds(threadKeepAliveSeconds);
    executor.setDaemon(false);
    executor.setCorePoolSize(threads);
    executor.setMaxPoolSize(threads);
    executor.setThreadPriority(Thread.MAX_PRIORITY);
    executor.setAllowCoreThreadTimeOut(true);
    executor.afterPropertiesSet();
    EventLoopGroup group;
    if (useEpoll) group = new EpollEventLoopGroup(threads, (Executor) executor);
    else group = new NioEventLoopGroup(threads, (Executor) executor);
    return group;
  }
}
