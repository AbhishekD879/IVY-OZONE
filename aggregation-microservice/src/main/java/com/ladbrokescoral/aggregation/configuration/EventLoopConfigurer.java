package com.ladbrokescoral.aggregation.configuration;

import io.netty.channel.EventLoopGroup;
import io.netty.channel.epoll.EpollEventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.util.NettyRuntime;
import java.util.concurrent.Executor;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

public class EventLoopConfigurer {

  private static final int KEEP_ALIVE = 3000;
  private static final int PROCESSOR_MULTIPLE = 2;

  public static EventLoopGroup getEventLoopGroup(
      boolean useEpoll, String threadNamePrefix, int maxThreads) {
    int threads = NettyRuntime.availableProcessors() * PROCESSOR_MULTIPLE;
    if (maxThreads != 0) threads = maxThreads;
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setThreadNamePrefix(threadNamePrefix);
    executor.setKeepAliveSeconds(KEEP_ALIVE);
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
