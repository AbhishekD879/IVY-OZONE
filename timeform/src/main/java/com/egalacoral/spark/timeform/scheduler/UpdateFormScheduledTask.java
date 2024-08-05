package com.egalacoral.spark.timeform.scheduler;

import com.egalacoral.spark.timeform.service.greyhound.TimeformBatchService;
import java.util.Date;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class UpdateFormScheduledTask {

  private static final Logger LOGGER = LoggerFactory.getLogger(UpdateFormScheduledTask.class);

  private TimeformBatchService timeformBatchService;

  @Autowired
  public UpdateFormScheduledTask(TimeformBatchService timeformBatchService) {
    this.timeformBatchService = timeformBatchService;
  }

  @Scheduled(cron = "${timeform.cron.scheduled.form}", zone = "${timeform.cron.timezone}")
  public void processGreyHounds() {
    LOGGER.info("Start updating greyhound form" + new Date());
    timeformBatchService.updateForm(new Date());
    LOGGER.info("Finish updating greyhound form " + new Date());
  }
}
