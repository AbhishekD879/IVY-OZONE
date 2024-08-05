package com.egalacoral.spark.timeform.scheduler.horseracing;

import com.egalacoral.spark.timeform.service.horseracing.HorseRacingBatchService;
import java.util.Date;
import org.joda.time.DateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/** Created by llegkyy on 15.09.16. */
@Component
public class ConsumeHRHorsesScheduledTask {
  private static final Logger LOGGER = LoggerFactory.getLogger(ConsumeHRHorsesScheduledTask.class);

  private HorseRacingBatchService horseRacingBatchService;

  @Autowired
  public ConsumeHRHorsesScheduledTask(HorseRacingBatchService horseRacingBatchService) {
    this.horseRacingBatchService = horseRacingBatchService;
  }

  @Scheduled(
      cron = "${timeform.cron.scheduled.horseracing.horses}",
      zone = "${timeform.cron.timezone}")
  public void processHorses() {
    LOGGER.info("Start horses task execution at {}", new Date());
    horseRacingBatchService.consumeHRHorses(new DateTime().plusDays(1).toDate());
    LOGGER.info("Finished horses task execution at {}", new Date());
  }

  @Scheduled(
      cron = "${timeform.cron.scheduled.horseracing.retry.horses}",
      zone = "${timeform.cron.timezone}")
  public void retryHorsesFetch() {
    Date date = new Date();
    LOGGER.info("Start horses task execution at {}", date);
    horseRacingBatchService.consumeHRHorses(date);
    LOGGER.info("Finished horses task execution at {}", new Date());
  }
}
