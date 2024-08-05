package com.coral.oxygen.middleware.scheduler;

import com.coral.oxygen.middleware.featured.consumer.FeaturedDataConsumer;
import com.coral.oxygen.middleware.featured.service.FeaturedDataProcessor;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModelsData;
import com.coral.oxygen.middleware.util.TrackUtils;
import com.ladbrokescoral.lib.leader.LeaderStatus;
import com.newrelic.api.agent.Trace;
import java.time.Instant;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@ConditionalOnProperty(name = "featured.scheduled.task.enabled")
public class ConsumeFeaturedDateScheduledTask extends ConsumeScheduledTask {
  private FeaturedDataConsumer featuredDataConsumer;
  private FeaturedDataProcessor dataProcessor;
  private LeaderStatus leaderStatus;

  @Autowired
  public ConsumeFeaturedDateScheduledTask(
      FeaturedDataConsumer featuredDataConsumer,
      FeaturedDataProcessor dataProcessor,
      LeaderStatus leaderStatus) {
    this.featuredDataConsumer = featuredDataConsumer;
    this.dataProcessor = dataProcessor;
    this.leaderStatus = leaderStatus;
  }

  @Scheduled(cron = "${featured.cron.expression}", zone = "${time.zone}")
  @Trace
  @Override
  public void process() {
    lastTimeLaunched = System.currentTimeMillis();
    try {
      if (leaderStatus.isLeaderNode()) {
        long start = System.currentTimeMillis();
        Instant lastRunTime = Instant.now();
        try {
          FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
          dataProcessor.process(data);
        } catch (Exception e) {
          log.error("Error during featured consumer task", e);
        } finally {
          TrackUtils.logDuration("featuredConsuming", start);
          dataProcessor.saveLastRunTime(lastRunTime.toEpochMilli());
          TrackUtils.logExcecutionTime("featuredConsuming", lastRunTime);
        }
      } else {
        slaveAction();
      }
    } catch (Exception e) {
      log.warn("Caught error while zookeeper leader election execution", e);
    }
  }

  private static void slaveAction() {
    log.info("Slave");
  }
}
