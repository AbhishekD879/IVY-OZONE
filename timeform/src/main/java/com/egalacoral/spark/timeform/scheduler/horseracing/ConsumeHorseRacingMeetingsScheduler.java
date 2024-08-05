package com.egalacoral.spark.timeform.scheduler.horseracing;

import com.egalacoral.spark.timeform.model.horseracing.HRMeeting;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingBatchService;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingStorageService;
import java.util.Date;
import java.util.Map;
import java.util.TimeZone;
import javax.annotation.PostConstruct;
import org.joda.time.DateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.scheduling.support.CronTrigger;
import org.springframework.scheduling.support.SimpleTriggerContext;
import org.springframework.stereotype.Component;

@Component
public class ConsumeHorseRacingMeetingsScheduler {

  private static final transient Logger LOGGER =
      LoggerFactory.getLogger(ConsumeHorseRacingMeetingsScheduler.class);

  private final HorseRacingBatchService batchService;
  private final HorseRacingStorageService storageService;

  private String cronExpression;
  private String timeZoneName;

  public ConsumeHorseRacingMeetingsScheduler(
      HorseRacingBatchService batchService, HorseRacingStorageService storageService) {
    this.batchService = batchService;
    this.storageService = storageService;
  }

  @PostConstruct
  public void consumeMeetingsOnStart() {
    LOGGER.info("Initial meetings consuming for today");
    consumeTodayMeetings();
    CronTrigger trigger = new CronTrigger(cronExpression, TimeZone.getTimeZone(timeZoneName));
    Date date = trigger.nextExecutionTime(new SimpleTriggerContext());
    DateTime today = new DateTime(new Date());
    DateTime nextTime = new DateTime(date);
    if (today.getDayOfYear() != nextTime.getDayOfYear()) {
      LOGGER.info("Initial meetings consuming for tomorrow");
      consumeTomorrowMeetings();
    }
  }

  @Scheduled(
      cron = "${timeform.cron.scheduled.horseracing.meetings}",
      zone = "${timeform.cron.timezone}")
  public void consumeMeetingsByScheduler() {
    LOGGER.info("Start consumeMeetingsByScheduler at {}", new Date());
    consumeTomorrowMeetings();
    LOGGER.info("Finish consumeMeetingsByScheduler at {}", new Date());
  }

  @Value("${timeform.cron.scheduled.horseracing.meetings}")
  public void setCronExpression(String cronExpression) {
    this.cronExpression = cronExpression;
  }

  @Value("${timeform.cron.timezone}")
  public void setTimeZoneName(String timeZoneName) {
    this.timeZoneName = timeZoneName;
  }

  private void fetchMeetingsForDateIfNotAvailable(Date date) {
    Map<HRMeeting.HRMeetingKey, HRMeeting> mapForDate = storageService.getMeetingsMapForDate(date);
    if (mapForDate == null || mapForDate.isEmpty()) {
      LOGGER.info("Consuming meetings for date {}", date);
      batchService.fetchMeetingsForDate(date);
    } else {
      LOGGER.info("{} meetings exists for date {}", mapForDate.size(), date);
    }
  }

  private void consumeTomorrowMeetings() {
    LOGGER.info("Start consumeTomorrowMeetings at {}", new Date());
    DateTime dateTime = new DateTime(new Date());
    dateTime = dateTime.plusDays(1);
    fetchMeetingsForDateIfNotAvailable(dateTime.toDate());
    LOGGER.info("Finish consumeTomorrowMeetings at {}", new Date());
  }

  private void consumeTodayMeetings() {
    LOGGER.info("Start consumeTodayMeetings at {}", new Date());
    fetchMeetingsForDateIfNotAvailable(new Date());
    LOGGER.info("Finish consumeTodayMeetings at {}", new Date());
  }
}
