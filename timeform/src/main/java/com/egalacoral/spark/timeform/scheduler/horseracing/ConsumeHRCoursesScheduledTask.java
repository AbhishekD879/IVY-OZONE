package com.egalacoral.spark.timeform.scheduler.horseracing;

import com.egalacoral.spark.timeform.service.horseracing.HorseRacingBatchService;
import java.util.Date;
import org.joda.time.DateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/** Created by llegkyy on 20.09.16. */
@Component
public class ConsumeHRCoursesScheduledTask {
  private static final Logger LOGGER = LoggerFactory.getLogger(ConsumeHRCoursesScheduledTask.class);

  private HorseRacingBatchService horseRacingBatchService;

  @Autowired
  public ConsumeHRCoursesScheduledTask(HorseRacingBatchService horseRacingBatchService) {
    this.horseRacingBatchService = horseRacingBatchService;
  }

  @Scheduled(
      cron = "${timeform.cron.scheduled.horseracing.courses}",
      zone = "${timeform.cron.timezone}")
  public void processCourses() {
    Date date = new Date();
    LOGGER.info("Start courses task execution at {}", date);
    horseRacingBatchService.consumeHRCourses(date);
    LOGGER.info("Finished courses task execution at {}", new Date());
  }

  @Scheduled(
      cron = "${timeform.cron.scheduled.horseracing.retry.courses}",
      zone = "${timeform.cron.timezone}")
  public void retryFetchCourses() {
    LOGGER.info("Start courses task execution at {}", new Date());
    horseRacingBatchService.consumeHRCourses(new DateTime().minusDays(1).toDate());
    LOGGER.info("Finished courses task execution at {}", new Date());
  }
}
