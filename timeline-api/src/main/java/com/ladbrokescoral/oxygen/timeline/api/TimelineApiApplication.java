package com.ladbrokescoral.oxygen.timeline.api;

import com.ladbrokescoral.oxygen.timeline.api.registrators.TimelineServiceRegistry;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.web.reactive.config.EnableWebFlux;

@SpringBootApplication
@EnableWebFlux
@Slf4j
public class TimelineApiApplication {

  public static void main(String[] args) {
    ConfigurableApplicationContext context =
        SpringApplication.run(TimelineApiApplication.class, args);
    startTimeLineApplication(context);
  }

  public static void startTimeLineApplication(ConfigurableApplicationContext context) {
    TimelineServiceRegistry serviceRegistry = context.getBean(TimelineServiceRegistry.class);
    try {
      serviceRegistry.load();
    } catch (Exception e) {
      log.error("Timeline Application startup failed.", e);
      serviceRegistry.stop();
      context.close();
      throw e;
    }
  }
}
