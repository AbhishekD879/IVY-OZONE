package com.coral.oxygen.edp.configuration;

import com.coral.oxygen.edp.exceptions.LiveServerException;
import com.coral.oxygen.edp.liveserv.OxyJsonMapper;
import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.client.Call;
import com.coral.oxygen.middleware.ms.liveserv.client.LiveServerCall;
import com.coral.oxygen.middleware.ms.liveserv.client.RetryableCall;
import com.coral.oxygen.middleware.ms.liveserv.impl.LiveServServiceImpl;
import com.coral.oxygen.middleware.ms.liveserv.impl.MessageHandlerMultiplexer;
import com.coral.oxygen.middleware.ms.liveserv.impl.SiteServEventIdResolver;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.time.Duration;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Created by azayats on 18.10.17. */
@Configuration
@Slf4j
public class LiveServConfiguration {

  @Bean
  public MessageHandlerMultiplexer messageHandlerMultiplexer() {
    return new MessageHandlerMultiplexer();
  }

  @Bean
  public SiteServEventIdResolver siteServEventIdResolver(SiteServerApi siteServerAPI) {
    return new SiteServEventIdResolver(siteServerAPI);
  }

  @Bean
  public Call call( //
      @Value("${liveserv.url}") String url, //
      @Value("${liveserv.timeout.connection}") long connectionTimeout, //
      @Value("${liveserv.timeout.read}") long readTimeout, //
      @Value("${retries.count}") int retriesCount, //
      @Value("${sleep.after.error.time}") long retriesDelay, //
      @Value("${liveserv.maxIdleConnections}") int maxIdleConnections, //
      @Value("${liveserv.keepAliveDuration}") long keepAliveDuration //
      ) {
    Call call;
    try {
      call =
          new LiveServerCall(
              url,
              connectionTimeout,
              readTimeout,
              maxIdleConnections,
              Duration.ofHours(keepAliveDuration));
    } catch (NoSuchAlgorithmException | KeyManagementException e) {
      String errorMsg = "Failed to construct LiveServerCall";
      log.error(errorMsg, e);
      throw new LiveServerException(errorMsg);
    }
    RetryableCall retriableCall = new RetryableCall(call);
    retriableCall.setRetriesCount(retriesCount);
    retriableCall.setRetriesDelay(retriesDelay);
    return retriableCall;
  }

  @Bean
  public LiveServService liveServService(
      Call call, MessageHandlerMultiplexer multiplexer, SiteServEventIdResolver idResolver) {
    LiveServService liveServService = new LiveServServiceImpl(call, multiplexer, idResolver);
    liveServService.startConsuming();
    return liveServService;
  }

  @Bean
  public OxyJsonMapper jsonMapper() {
    return new OxyJsonMapper(new ObjectMapper());
  }
}
