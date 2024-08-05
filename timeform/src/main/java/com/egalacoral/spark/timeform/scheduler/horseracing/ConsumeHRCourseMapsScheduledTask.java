package com.egalacoral.spark.timeform.scheduler.horseracing;

import com.egalacoral.spark.timeform.service.horseracing.HorseRacingBatchService;
import java.util.Date;
import org.joda.time.DateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class ConsumeHRCourseMapsScheduledTask {
  private static final Logger LOGGER =
      LoggerFactory.getLogger(ConsumeHRCourseMapsScheduledTask.class);

  private HorseRacingBatchService horseRacingBatchService;

  @Autowired
  public ConsumeHRCourseMapsScheduledTask(HorseRacingBatchService horseRacingBatchService) {
    this.horseRacingBatchService = horseRacingBatchService;
  }

  @Scheduled(
      cron = "${timeform.cron.scheduled.horseracing.coursemaps.today}",
      zone = "${timeform.cron.timezone}")
  public void consumeTodayCourseMaps() {
    Date date = new Date();
    LOGGER.info("Start today course maps consuming task execution at {}", date);
    horseRacingBatchService.consumeCourseMaps(date);
    LOGGER.info("Finished today course maps consuming task execution at {}", new Date());
  }

  @Scheduled(
      cron = "${timeform.cron.scheduled.horseracing.coursemaps.tomorrow}",
      zone = "${timeform.cron.timezone}")
  public void consumeTomorrowCourseMaps() {
    Date date = new Date();
    LOGGER.info("Start tomorrow course maps consuming task execution at {}", date);
    horseRacingBatchService.consumeCourseMaps(new DateTime().plusDays(1).toDate());
    LOGGER.info("Finished tomorrow course maps consuming task execution at {}", new Date());
  }
}
