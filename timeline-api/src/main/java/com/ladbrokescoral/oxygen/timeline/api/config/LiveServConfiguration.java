package com.ladbrokescoral.oxygen.timeline.api.config;

import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.client.Call;
import com.coral.oxygen.middleware.ms.liveserv.client.LiveServerCall;
import com.coral.oxygen.middleware.ms.liveserv.client.RetryableCall;
import com.coral.oxygen.middleware.ms.liveserv.impl.LiveServServiceImpl;
import com.coral.oxygen.middleware.ms.liveserv.impl.ManagedLiveServeService;
import com.coral.oxygen.middleware.ms.liveserv.impl.MessageHandlerMultiplexer;
import com.coral.oxygen.middleware.ms.liveserv.impl.SiteServEventIdResolver;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.time.Duration;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class LiveServConfiguration {

  @Value("${siteServer.api.latest.version}")
  private String latestApiVersion;

  @Value("${siteServer.priceboost.enabled}")
  private boolean isPriceBoostEnabled;

  @Value("${siteServer.api.version}")
  private String apiVersion;

  @Bean
  public SiteServerApi siteServerApi(
      @Value("${siteServer.base.url}") String siteServerUrl,
      @Value("${siteServer.connection.timeout}") int connectionTimeout,
      @Value("${siteServer.read.timeout}") int readTimeout,
      @Value("${siteServer.retries.number}") int retriesNumber,
      @Value("${siteServer.logging.level}") String loggingLevel)
      throws NoSuchAlgorithmException, KeyManagementException {
    return new SiteServerApi.Builder()
        .setUrl(siteServerUrl)
        .setLoggingLevel(SiteServerApi.Level.valueOf(loggingLevel))
        .setConnectionTimeout(connectionTimeout)
        .setReadTimeout(readTimeout)
        .setMaxNumberOfRetries(retriesNumber)
        .setVersion(getapiVersion())
        .build();
  }

  private String getapiVersion() {
    if (isPriceBoostEnabled) {
      return latestApiVersion;
    }
    return apiVersion;
  }

  @Bean
  public MessageHandlerMultiplexer messageHandlerMultiplexer(MessageHandler messageHandler) {
    MessageHandlerMultiplexer messageHandlerMultiplexer = new MessageHandlerMultiplexer();
    messageHandlerMultiplexer.addMessageHandler(messageHandler);
    return messageHandlerMultiplexer;
  }

  @Bean
  public SiteServEventIdResolver siteServEventIdResolver(SiteServerApi siteServerApi) {
    return new SiteServEventIdResolver(siteServerApi);
  }

  @Bean
  public Call call(
      @Value("${liveserv.url}") String url,
      @Value("${liveserv.timeout.connection}") long connectionTimeout,
      @Value("${liveserv.timeout.read}") long readTimeout,
      @Value("${retries.count}") int retriesCount,
      @Value("${sleep.after.error.time}") long retriesDelay,
      @Value("${liveserv.maxIdleConnections}") int maxIdleConnections,
      @Value("${liveserv.keepAliveDuration}") long keepAliveDuration)
      throws KeyManagementException, NoSuchAlgorithmException {
    RetryableCall retryableCall =
        new RetryableCall(
            new LiveServerCall(
                url,
                connectionTimeout,
                readTimeout,
                maxIdleConnections,
                Duration.ofHours(keepAliveDuration)));
    retryableCall.setRetriesCount(retriesCount);
    retryableCall.setRetriesDelay(retriesDelay);
    return retryableCall;
  }

  @Bean
  public ManagedLiveServeService managedLiveServeService(
      Call call, MessageHandlerMultiplexer multiplexer, SiteServEventIdResolver idResolver) {
    ManagedLiveServeService managedLiveServeService =
        new LiveServServiceImpl(call, multiplexer, idResolver);
    managedLiveServeService.startConsuming();
    return managedLiveServeService;
  }
}
