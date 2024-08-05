package com.ladbrokescoral.oxygen.trendingbets.configuration;

import io.netty.channel.EventLoopGroup;
import io.netty.channel.epoll.EpollEventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.util.NettyRuntime;
import java.util.concurrent.Executor;
import lombok.experimental.UtilityClass;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@Slf4j
@UtilityClass
public class EventLoopHelper {

  private static final int THREAD_FACTOR = 2;

  private static final int KEEP_ALIVE_SECONDS = 3000;

  public static EventLoopGroup getEventLoopGroup(
      boolean useEpoll, String threadNamePrefix, int numberOfThreads) {

    int threads = NettyRuntime.availableProcessors() * THREAD_FACTOR;
    if (numberOfThreads != 0) threads = numberOfThreads;
    log.info("EventLoopGroup:: Threads created:: {}", threads);
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setThreadNamePrefix(threadNamePrefix);
    executor.setKeepAliveSeconds(KEEP_ALIVE_SECONDS);
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
