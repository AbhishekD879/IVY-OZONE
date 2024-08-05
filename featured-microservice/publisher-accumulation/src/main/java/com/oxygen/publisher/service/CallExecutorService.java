package com.oxygen.publisher.service;

import com.newrelic.api.agent.NewRelic;
import com.oxygen.health.api.ReloadableService;
import com.oxygen.publisher.translator.ChainFactory;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import lombok.extern.slf4j.Slf4j;

/** Created by Aliaksei Yarotski on 1/2/18. */
@Slf4j
public class CallExecutorService implements ReloadableService {

  private AtomicBoolean isOnService = new AtomicBoolean();
  private ScheduledExecutorService executorService;
  private ChainFactory chainFactory;
  private long executionPeriod;

  public CallExecutorService(ChainFactory chainFactory, long executionPeriod) {
    this.chainFactory = chainFactory;
    this.executionPeriod = executionPeriod;
    this.executorService = Executors.newSingleThreadScheduledExecutor();
  }

  @Override
  public void start() {
    isOnService.set(true);
    executorService.scheduleAtFixedRate(this::doExecute, 0, executionPeriod, TimeUnit.SECONDS);
  }

  @Override
  public void evict() {
    log.info("[CallExecutorService] service is reloading ...");
    this.executorService = Executors.newSingleThreadScheduledExecutor();
    isOnService.set(false);
  }

  @Override
  public boolean isHealthy() {
    return isOnService.get() && !executorService.isTerminated() && !executorService.isShutdown();
  }

  @Override
  public void onFail(Exception ex) {
    isOnService.set(false);
  }

  private void doExecute() {
    try {
      log.info("CallExecutor started new job.");
      chainFactory.getScheduledJob().start(null);
      isOnService.set(true);
    } catch (Exception e) {
      log.error("Error while requesting new version.", e);
      NewRelic.noticeError(e);
      isOnService.set(false);
    }
  }
}
