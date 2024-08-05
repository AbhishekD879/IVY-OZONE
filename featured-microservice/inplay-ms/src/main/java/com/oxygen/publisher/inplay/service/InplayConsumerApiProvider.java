package com.oxygen.publisher.inplay.service;

import com.newrelic.api.agent.NewRelic;
import com.oxygen.health.api.ReloadableService;
import com.oxygen.publisher.service.RetrofitClientFactory;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Slf4j
@RequiredArgsConstructor
@Component
public class InplayConsumerApiProvider implements ReloadableService {

  private AtomicReference<InplayConsumerApi> inplayConsumerApi = new AtomicReference<>();
  private AtomicBoolean isOnService = new AtomicBoolean();

  private final RetrofitClientFactory retrofitClientFactory;

  @Value("${inplay.consumer.host}")
  private String inplayConsumerHost;

  @Value("${inplay.consumer.port}")
  private Integer inplayConsumerPort;

  @Override
  public void start() {

    inplayConsumerApi.set(
        retrofitClientFactory.createClient(
            inplayConsumerHost, inplayConsumerPort, InplayConsumerApi.class));
    isOnService.set(true);
    log.info("Started FeaturedApiProvider {}:{}", inplayConsumerHost, inplayConsumerPort);
  }

  @Override
  public void evict() {
    // No Implementation provided
  }

  @Override
  public boolean isHealthy() {
    return isOnService.get();
  }

  @Override
  public void onFail(Exception ex) {
    log.error("Failed on middleware call.", ex);
    NewRelic.noticeError(ex);
    isOnService.set(false);
  }

  public InplayConsumerApi getInplayConsumerApi() {
    return inplayConsumerApi.get();
  }
}
