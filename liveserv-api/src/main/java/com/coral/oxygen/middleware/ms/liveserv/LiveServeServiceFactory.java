package com.coral.oxygen.middleware.ms.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.client.Call;
import com.coral.oxygen.middleware.ms.liveserv.impl.ChunkedLiveServServiceImpl;
import com.coral.oxygen.middleware.ms.liveserv.impl.EventIdResolver;
import com.coral.oxygen.middleware.ms.liveserv.impl.LiveServServiceImpl;
import com.coral.oxygen.middleware.ms.liveserv.impl.ManagedLiveServeService;
import java.time.Duration;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;

public class LiveServeServiceFactory {

  public LiveServService createSimpleLiveServeService(
      Call call, MessageHandler messageHandler, EventIdResolver eventIdResolver) {
    return new LiveServServiceImpl(call, messageHandler, eventIdResolver);
  }

  public LiveServService createCachingLiveServeService(
      Call call,
      MessageHandler messageHandler,
      EventIdResolver eventIdResolver,
      long subscriptionsSize,
      long ttlSeconds) {
    return createManagedLiveServeService(
        call,
        messageHandler,
        eventIdResolver,
        subscriptionsSize,
        Duration.ofSeconds(ttlSeconds),
        Executors.newSingleThreadScheduledExecutor());
  }

  private ManagedLiveServeService createManagedLiveServeService(
      Call call,
      MessageHandler messageHandler,
      EventIdResolver eventIdResolver,
      long subscriptionsSize,
      Duration subscriptionsTtl,
      ScheduledExecutorService scheduledExecutor) {
    return new LiveServServiceImpl(
        call,
        messageHandler,
        eventIdResolver,
        subscriptionsSize,
        subscriptionsTtl,
        scheduledExecutor);
  }

  public LiveServService createChunkedLiveServeService(
      Call call,
      MessageHandler messageHandler,
      EventIdResolver eventIdResolver,
      long chunkSize,
      Duration subscriptionsTtl,
      ScheduledExecutorService scheduledExecutor) {
    return new ChunkedLiveServServiceImpl(
        () ->
            createManagedLiveServeService(
                call,
                messageHandler,
                eventIdResolver,
                chunkSize,
                subscriptionsTtl,
                scheduledExecutor),
        chunkSize);
  }
}
