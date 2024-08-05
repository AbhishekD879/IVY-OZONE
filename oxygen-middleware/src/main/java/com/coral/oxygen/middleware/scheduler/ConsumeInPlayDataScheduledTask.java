package com.coral.oxygen.middleware.scheduler;

import com.coral.oxygen.middleware.in_play.service.InPlayDataProcessor;
import com.coral.oxygen.middleware.util.TrackUtils;
import com.ladbrokescoral.lib.leader.LeaderStatus;
import com.newrelic.api.agent.Trace;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@ConditionalOnProperty(name = "inplay.scheduled.task.enabled")
public class ConsumeInPlayDataScheduledTask extends ConsumeScheduledTask {

  private InPlayDataProcessor inPlayDataProcessor;
  private LeaderStatus leaderStatus;

  @Autowired
  public ConsumeInPlayDataScheduledTask(
      InPlayDataProcessor inPlayDataProcessor, LeaderStatus leaderStatus) {
    this.inPlayDataProcessor = inPlayDataProcessor;
    this.leaderStatus = leaderStatus;
  }

  @Scheduled(cron = "${inplay.cron.expression}", zone = "${time.zone}")
  @Trace
  @Override
  public void process() throws InterruptedException {
    lastTimeLaunched = System.currentTimeMillis();
    try {
      if (leaderStatus.isLeaderNode()) {
        log.info("Started inPlay consuming process");
        long start = System.currentTimeMillis();

        inPlayDataProcessor.tryProcess();

        TrackUtils.logDuration("inplayConsuming", start);
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
