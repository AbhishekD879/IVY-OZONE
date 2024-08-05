package com.egalacoral.spark.timeform.scheduler;

import com.egalacoral.spark.timeform.service.greyhound.TimeformBatchService;
import java.util.Date;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/** Created by Igor.Domshchikov on 8/22/2016. */
@Component
public class ConsumePerformancesScheduledTask {

  private TimeformBatchService timeformBatchService;

  private static final Logger LOGGER =
      LoggerFactory.getLogger(ConsumePerformancesScheduledTask.class);

  @Autowired
  public ConsumePerformancesScheduledTask(TimeformBatchService timeformBatchService) {
    this.timeformBatchService = timeformBatchService;
  }

  @Scheduled(
      cron = "${timeform.cron.scheduled.greyhoundracing.performances}",
      zone = "${timeform.cron.timezone}")
  public void processPerformances() {
    LOGGER.info("Start task execution at " + new Date());
    timeformBatchService.consumePerformances(new Date());
    LOGGER.info("Finished task execution at " + new Date());
  }

  @Scheduled(
      cron = "${timeform.cron.scheduled.greyhoundracing.performances.last}",
      zone = "${timeform.cron.timezone}")
  public void processPerformancesLastTime() {
    processPerformances();
  }
}
