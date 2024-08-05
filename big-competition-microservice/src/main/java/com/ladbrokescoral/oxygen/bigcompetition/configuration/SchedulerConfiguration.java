package com.ladbrokescoral.oxygen.bigcompetition.configuration;

import com.newrelic.api.agent.NewRelic;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.TaskScheduler;
import org.springframework.scheduling.concurrent.ConcurrentTaskScheduler;

@Configuration
// @Slf4j
public class SchedulerConfiguration {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Bean
  public TaskScheduler taskScheduler() {
    ConcurrentTaskScheduler scheduler = new ConcurrentTaskScheduler();
    scheduler.setErrorHandler(
        (Throwable throwable) -> {
          ASYNC_LOGGER.error("Error during processing", throwable);
          NewRelic.noticeError(throwable);
        });
    return scheduler;
  }
}
