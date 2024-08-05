package com.egalacoral.spark.timeform.scheduler.horseracing;

import com.egalacoral.spark.timeform.service.horseracing.HorseRacingBatchService;
import java.util.Date;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/** Created by llegkyy on 01.09.16. */
@Component
public class ConsumeHRPerformancesScheduledTask {

  private HorseRacingBatchService horseRacingBatchService;

  private static final Logger LOGGER =
      LoggerFactory.getLogger(ConsumeHRPerformancesScheduledTask.class);

  @Autowired
  public ConsumeHRPerformancesScheduledTask(HorseRacingBatchService timeformBatchService) {
    this.horseRacingBatchService = timeformBatchService;
  }

  @Scheduled(
      cron = "${timeform.cron.scheduled.horseracing.performances}",
      zone = "${timeform.cron.timezone}")
  public void processPerformances() {
    LOGGER.info("Start horseracing.performances task execution at " + new Date());
    horseRacingBatchService.consumeHRPerformances(new Date());
    LOGGER.info("Finished horseracing.performances task execution at " + new Date());
  }
}
