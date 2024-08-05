package com.egalacoral.spark.timeform.scheduler.horseracing;

import com.egalacoral.spark.timeform.service.horseracing.HorseRacingBatchService;
import java.util.Date;
import javax.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/** Created by llegkyy on 21.09.16. */
@Component
public class ConsumeHRCountriesScheduledTask {
  private static final Logger LOGGER =
      LoggerFactory.getLogger(ConsumeHRCountriesScheduledTask.class);

  private HorseRacingBatchService horseRacingBatchService;

  @Autowired
  public ConsumeHRCountriesScheduledTask(HorseRacingBatchService horseRacingBatchService) {
    this.horseRacingBatchService = horseRacingBatchService;
  }

  @Scheduled(
      cron = "${timeform.cron.scheduled.horseracing.countries}",
      zone = "${timeform.cron.timezone}")
  public void processCountries() {
    LOGGER.info("Start horses countries task execution at {}", new Date());
    horseRacingBatchService.consumeHRCountries(new Date());
    LOGGER.info("Finished horses countries task execution at {}", new Date());
  }

  @PostConstruct
  public void init() {
    LOGGER.info("Start horses countries task execution at {}", new Date());
    horseRacingBatchService.consumeHRCountries(new Date());
    LOGGER.info("Finished horses countries task execution at {}", new Date());
  }
}
