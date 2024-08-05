package com.egalacoral.spark.timeform.scheduler;

import com.egalacoral.spark.timeform.service.greyhound.TimeformBatchService;
import java.util.Date;
import org.joda.time.DateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class ConsumeRacesWithEntriesScheduledTask {

  private static final Logger LOGGER =
      LoggerFactory.getLogger(ConsumeRacesWithEntriesScheduledTask.class);

  private TimeformBatchService timeformBatchService;

  @Autowired
  public ConsumeRacesWithEntriesScheduledTask(TimeformBatchService timeformBatchService) {
    this.timeformBatchService = timeformBatchService;
  }

  @Scheduled(cron = "${timeform.cron.scheduled.today.entries}", zone = "${timeform.cron.timezone}")
  public void processTodayEntries() {
    LOGGER.info("Start task execution at " + new Date());
    Date currentTime = new Date();
    timeformBatchService.consumeRacesWithEntries(currentTime);
    LOGGER.info("Finished task execution at " + new Date());
  }

  @Scheduled(
      cron = "${timeform.cron.scheduled.tomorrow.entries}",
      zone = "${timeform.cron.timezone}")
  public void processTomorrowEntries() {
    LOGGER.info("Start task execution at " + new Date());
    DateTime nextDay = new DateTime(new Date());
    timeformBatchService.consumeRacesWithEntries(nextDay.plusDays(1).toDate());
    LOGGER.info("Finished task execution at " + new Date());
  }
}
