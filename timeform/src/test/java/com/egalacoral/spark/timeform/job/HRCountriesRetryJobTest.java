package com.egalacoral.spark.timeform.job;

import com.egalacoral.spark.timeform.service.horseracing.HorseRacingBatchService;
import org.junit.Test;
import org.mockito.Mockito;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;

public class HRCountriesRetryJobTest {

  private HorseRacingBatchService horseRacingBatchService;

  @Test
  public void testExecute() throws JobExecutionException {
    horseRacingBatchService = Mockito.mock(HorseRacingBatchService.class);
    HRCountriesRetryJob job = new HRCountriesRetryJob();
    job.setHorseRacingBatchService(horseRacingBatchService);
    JobExecutionContext context = Mockito.mock(JobExecutionContext.class);
    job.execute(context);

    Mockito.verify(horseRacingBatchService, Mockito.times(1)).consumeHRCountries(Mockito.any());
  }
}
