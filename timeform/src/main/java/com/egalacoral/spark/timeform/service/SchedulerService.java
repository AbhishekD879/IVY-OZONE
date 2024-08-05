package com.egalacoral.spark.timeform.service;

import com.egalacoral.spark.timeform.job.HRCountriesRetryJob;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.TimeZone;
import org.quartz.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class SchedulerService {

  private static final Logger LOGGER = LoggerFactory.getLogger(SchedulerService.class);

  private Scheduler scheduler;

  @Autowired
  public SchedulerService(Scheduler scheduler) {
    this.scheduler = scheduler;
  }

  private static final String HR_COUNTRIES_JOB_NAME = "retry horse racing countries fetch";
  private static final String HR_COUNTRIES_TRIGGER_NAME =
      "retry horse racing countries fetch trigger";

  private Map<String, JobKey> scheduledJobs = new HashMap<>();

  public void scheduleHRCountriesRetry() {
    removeJob(HR_COUNTRIES_JOB_NAME);
    JobDetail jobDetail =
        JobBuilder.newJob(HRCountriesRetryJob.class).withIdentity(HR_COUNTRIES_JOB_NAME).build();
    scheduledJobs.put(HR_COUNTRIES_JOB_NAME, jobDetail.getKey());
    Trigger trigger =
        TriggerBuilder.newTrigger()
            .withIdentity(HR_COUNTRIES_TRIGGER_NAME)
            .withSchedule(
                CronScheduleBuilder.cronSchedule("0 0 * * * ?")
                    .inTimeZone(TimeZone.getTimeZone("Europe/London")))
            .build();
    try {
      Date date = scheduler.scheduleJob(jobDetail, trigger);
      LOGGER.info("next HR countries fetch plan on {}", date);
    } catch (SchedulerException e) {
      LOGGER.error("could not schedule " + HR_COUNTRIES_JOB_NAME + " due to: {}", e.getMessage());
    }
  }

  public void unscheduleHRCountriesRetry() {
    removeJob(HR_COUNTRIES_JOB_NAME);
  }

  private void removeJob(String jobName) {
    try {
      scheduler.deleteJob(scheduledJobs.get(jobName));
      LOGGER.info("{} job was deleted", jobName);
    } catch (SchedulerException e) {
      LOGGER.error("{} job could not be removed due to {}", jobName, e.getMessage());
    }
  }
}
