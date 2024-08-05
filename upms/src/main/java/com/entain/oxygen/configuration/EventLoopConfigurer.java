package com.entain.oxygen.configuration;

import io.netty.channel.EventLoopGroup;
import io.netty.channel.epoll.EpollEventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.util.NettyRuntime;
import java.util.concurrent.Executor;
import lombok.experimental.UtilityClass;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@UtilityClass
public class EventLoopConfigurer {

  private static final int PROCESSORS = 2;
  private static final int KEEP_ALIVE = 3000;

  public static EventLoopGroup getEventLoopGroup(String threadNamePrefix, int numberOfThreads) {

    int threads = NettyRuntime.availableProcessors() * PROCESSORS;
    if (numberOfThreads != 0) threads = numberOfThreads;
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setThreadNamePrefix(threadNamePrefix);
    executor.setKeepAliveSeconds(KEEP_ALIVE);
    executor.setDaemon(false);
    executor.setCorePoolSize(threads);
    executor.setMaxPoolSize(threads);
    executor.setThreadPriority(Thread.MAX_PRIORITY);
    executor.setAllowCoreThreadTimeOut(true);
    executor.afterPropertiesSet();
    if (System.getProperty("os.name").equalsIgnoreCase("Linux"))
      return new EpollEventLoopGroup(threads, (Executor) executor);
    return new NioEventLoopGroup(threads, (Executor) executor);
  }
}
