package com.egalacoral.spark.timeform.scheduler;

import com.egalacoral.spark.timeform.service.greyhound.TimeformBatchService;
import java.util.Calendar;
import java.util.Date;
import java.util.TimeZone;
import javax.annotation.PostConstruct;
import org.joda.time.DateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/** Created by Igor.Domshchikov on 8/8/2016. */
@Component
public class RequestMeetingScheduledTask {

  private static final Logger LOGGER = LoggerFactory.getLogger(RequestMeetingScheduledTask.class);

  private TimeformBatchService timeformBatchService;

  @Autowired
  public RequestMeetingScheduledTask(TimeformBatchService timeformBatchService) {
    this.timeformBatchService = timeformBatchService;
  }

  @PostConstruct
  public void init() {
    Date date = determineFetchDate(new Date());
    timeformBatchService.processMeetings(date);
  }

  @Scheduled(cron = "${timeform.cron.scheduled.time}", zone = "${timeform.cron.timezone}")
  public void processMeetings() {
    LOGGER.info("Start task execution at " + new Date());
    DateTime nextDay = new DateTime(new Date());
    nextDay = nextDay.plusDays(1);
    timeformBatchService.processMeetings(nextDay.toDate());
    LOGGER.info("Finished task execution at " + new Date());
  }

  private Date determineFetchDate(Date date) {
    Calendar template = Calendar.getInstance();
    template.setTimeZone(TimeZone.getTimeZone("Europe/London"));
    template.set(Calendar.HOUR_OF_DAY, 16);
    template.set(Calendar.MINUTE, 0);

    Calendar currentDate = Calendar.getInstance();
    currentDate.setTimeZone(TimeZone.getTimeZone("Europe/London"));
    currentDate.setTime(date);

    if (currentDate.before(template)) {
      return date;
    } else {
      return new DateTime(date).plusDays(1).toDate();
    }
  }
}
