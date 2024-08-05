package com.egalacoral.spark.timeform.scheduler;

import com.egalacoral.spark.timeform.service.greyhound.TimeformBatchService;
import java.util.Date;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/** Created by Igor.Domshchikov on 8/19/2016. */
@Component
public class ConsumeGreyhoundsScheduledTask {

  private static final Logger LOGGER =
      LoggerFactory.getLogger(ConsumeGreyhoundsScheduledTask.class);

  private TimeformBatchService timeformBatchService;

  @Autowired
  public ConsumeGreyhoundsScheduledTask(TimeformBatchService timeformBatchService) {
    this.timeformBatchService = timeformBatchService;
  }

  @Scheduled(cron = "${timeform.cron.scheduled.greyhounds}", zone = "${timeform.cron.timezone}")
  public void processGreyHounds() {
    LOGGER.info("Start greyhounds task execution at " + new Date());
    timeformBatchService.consumeGreyhounds(new Date());
    LOGGER.info("Finished greyhounds task execution at " + new Date());
  }
}
