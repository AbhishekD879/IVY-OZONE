package com.egalacoral.spark.timeform.scheduler;

import com.egalacoral.spark.timeform.service.greyhound.TimeformBatchService;
import java.util.Date;
import org.joda.time.DateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/** Created by Igor.Domshchikov on 8/26/2016. */
@Component
public class ConsumeTracksScheduledTask {

  private static final Logger LOGGER = LoggerFactory.getLogger(ConsumeTracksScheduledTask.class);

  private TimeformBatchService timeformBatchService;

  @Scheduled(cron = "${timeform.cron.scheduled.tracks}", zone = "${timeform.cron.timezone}")
  public void processTracks() {
    Date date = new Date();
    LOGGER.info("Start task execution at " + date);
    timeformBatchService.consumeTracks(date);
    LOGGER.info("Finished task execution at " + new Date());
  }

  @Scheduled(cron = "${timeform.cron.scheduled.retry.tracks}", zone = "${timeform.cron.timezone}")
  public void retryFetchTracks() {
    LOGGER.info("Start task execution at " + new Date());
    timeformBatchService.consumeTracks(DateTime.now().minusDays(1).toDate());
    LOGGER.info("Finished task execution at " + new Date());
  }

  @Autowired
  public void setTimeformBatchService(TimeformBatchService timeformBatchService) {
    this.timeformBatchService = timeformBatchService;
  }
}
