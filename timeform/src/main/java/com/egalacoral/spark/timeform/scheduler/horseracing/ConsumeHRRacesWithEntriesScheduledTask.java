package com.egalacoral.spark.timeform.scheduler.horseracing;

import static java.util.TimeZone.getTimeZone;

import com.egalacoral.spark.timeform.service.horseracing.HorseRacingBatchService;
import java.util.Calendar;
import java.util.Date;
import org.joda.time.DateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class ConsumeHRRacesWithEntriesScheduledTask {
  private static final Logger LOGGER =
      LoggerFactory.getLogger(ConsumeHRRacesWithEntriesScheduledTask.class);

  private HorseRacingBatchService horseRacingBatchService;

  @Autowired
  public ConsumeHRRacesWithEntriesScheduledTask(HorseRacingBatchService horseRacingBatchService) {
    this.horseRacingBatchService = horseRacingBatchService;
  }

  @Scheduled(cron = "${timeform.cron.scheduled.hr.today.races}", zone = "${timeform.cron.timezone}")
  public void processTodayHRRacesWithEntries() {
    Date date = new Date();
    LOGGER.info("Start consuming Races with Entries for today at " + new Date());
    horseRacingBatchService.fetchRacesWithEntriesForDate(date);
    LOGGER.info("Finished consuming Races with Entries task" + new Date());
  }

  @Scheduled(
      cron = "${timeform.cron.scheduled.hr.tomorrow.races}",
      zone = "${timeform.cron.timezone}")
  public void processTomorrowHRRacesWithEntries() {
    Date date = new Date();
    if (verifyDate(date)) {
      Date tomorrow = new DateTime(date).plusDays(1).toDate();
      LOGGER.info(
          "Start consuming Races with Entries for tomorrow date {} at {}", tomorrow, new Date());
      horseRacingBatchService.fetchRacesWithEntriesForDate(tomorrow);
      LOGGER.info("Finished consuming Races with Entries task" + new Date());
    }
  }

  private boolean verifyDate(Date date) {
    Calendar template = Calendar.getInstance();
    template.setTimeZone(getTimeZone("Europe/London"));
    template.set(Calendar.HOUR_OF_DAY, 15);
    template.set(Calendar.MINUTE, 35);

    Calendar currentDate = Calendar.getInstance();
    currentDate.setTimeZone(getTimeZone("Europe/London"));
    currentDate.setTime(date);

    if (currentDate.before(template)) {
      return false;
    }
    return true;
  }
}
