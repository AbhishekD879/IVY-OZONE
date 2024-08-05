package com.egalacoral.spark.timeform.job;

import com.egalacoral.spark.timeform.service.horseracing.HorseRacingBatchService;
import java.util.Date;
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class HRCountriesRetryJob implements Job {

  private static final Logger LOGGER = LoggerFactory.getLogger(HRCountriesRetryJob.class);

  private HorseRacingBatchService horseRacingBatchService;

  @Override
  public void execute(JobExecutionContext context) throws JobExecutionException {
    LOGGER.info("Run retry for horse racing countries fetch");
    horseRacingBatchService.consumeHRCountries(new Date());
  }

  @Autowired
  public void setHorseRacingBatchService(HorseRacingBatchService horseRacingBatchService) {
    this.horseRacingBatchService = horseRacingBatchService;
  }
}
