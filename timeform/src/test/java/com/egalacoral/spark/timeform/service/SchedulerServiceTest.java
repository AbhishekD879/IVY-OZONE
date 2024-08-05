package com.egalacoral.spark.timeform.service;

import org.junit.Test;
import org.mockito.Mockito;
import org.quartz.Scheduler;
import org.quartz.SchedulerException;

public class SchedulerServiceTest {

  private Scheduler scheduler;

  @Test
  public void testScheduleHRCountriesRetry() throws SchedulerException {
    scheduler = Mockito.mock(Scheduler.class);
    SchedulerService schedulerService = new SchedulerService(scheduler);

    schedulerService.scheduleHRCountriesRetry();
    Mockito.verify(scheduler, Mockito.times(1)).deleteJob(Mockito.any());
    Mockito.verify(scheduler, Mockito.times(1)).scheduleJob(Mockito.any(), Mockito.any());
  }
}
