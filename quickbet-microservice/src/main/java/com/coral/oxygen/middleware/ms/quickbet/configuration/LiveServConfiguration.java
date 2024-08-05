package com.coral.oxygen.middleware.ms.quickbet.configuration;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.LiveServeServiceFactory;
import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.client.Call;
import com.coral.oxygen.middleware.ms.liveserv.client.LiveServerCall;
import com.coral.oxygen.middleware.ms.liveserv.client.RetryableCall;
import com.coral.oxygen.middleware.ms.liveserv.impl.MessageHandlerMultiplexer;
import com.coral.oxygen.middleware.ms.liveserv.impl.SiteServEventIdResolver;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.time.Duration;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.ThreadPoolTaskScheduler;

@Configuration
public class LiveServConfiguration {

  @Bean
  public MessageHandlerMultiplexer messageHandlerMultiplexer(MessageHandler messageHandler) {
    MessageHandlerMultiplexer messageHandlerMultiplexer = new MessageHandlerMultiplexer();
    messageHandlerMultiplexer.addMessageHandler(messageHandler);
    return messageHandlerMultiplexer;
  }

  @Bean
  public SiteServEventIdResolver siteServEventIdResolver(SiteServerApi siteServerAPI) {
    return new SiteServEventIdResolver(siteServerAPI);
  }

  @Bean
  public Call call(
      @Value("${liveserv.url}") String url,
      @Value("${liveserv.timeout.connection}") long connectionTimeout,
      @Value("${liveserv.call.pool.idle}") int idlePoolSize,
      @Value("${liveserv.call.pool.idle.ttl.seconds}") long idleConnectionTime,
      @Value("${liveserv.timeout.read}") long readTimeout,
      @Value("${retries.count}") int retriesCount,
      @Value("${sleep.after.error.time}") long retriesDelay)
      throws KeyManagementException, NoSuchAlgorithmException {
    Call call =
        new LiveServerCall(
            url,
            connectionTimeout,
            readTimeout,
            idlePoolSize,
            Duration.ofSeconds(idleConnectionTime));
    RetryableCall retriableCall = new RetryableCall(call);
    retriableCall.setRetriesCount(retriesCount);
    retriableCall.setRetriesDelay(retriesDelay);
    return retriableCall;
  }

  @Bean
  public LiveServService liveServService(
      Call call,
      MessageHandlerMultiplexer multiplexer,
      SiteServEventIdResolver idResolver,
      @Qualifier("threadPoolTaskScheduler") ThreadPoolTaskScheduler threadPoolTaskScheduler,
      @Value("${liveserv.subscriptions.limitPerClient:350}") long subscriptionsMaxCount,
      @Value("${liveserv.subscriptions.ttl.seconds:1200}") long subscriptionsTtl,
      @Value("${liveserv.subscriptions.maintenance.threads:1}") int maintenanceThreads) {
    LiveServService liveServService =
        new LiveServeServiceFactory()
            .createChunkedLiveServeService(
                call,
                multiplexer,
                idResolver,
                subscriptionsMaxCount,
                Duration.ofSeconds(subscriptionsTtl),
                threadPoolTaskScheduler.getScheduledExecutor());
    liveServService.startConsuming();
    return liveServService;
  }
}
