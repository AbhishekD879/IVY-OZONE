package com.coral;

import com.coral.oxygen.middleware.ms.quickbet.connector.SocketIOConnector;
import com.newrelic.api.agent.NewRelic;
import lombok.Generated;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.scheduling.annotation.EnableScheduling;

/** Created by oleg.perushko@symphony-solutions.eu on 4/19/17. */
@SpringBootApplication
@EnableScheduling
public class Application {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Generated
  public static void main(String[] args) {
    ConfigurableApplicationContext context = SpringApplication.run(Application.class, args);
    SocketIOConnector connector = context.getBean(SocketIOConnector.class);
    try {
      connector.start();
    } catch (Exception e) {
      NewRelic.noticeError(e);
      ASYNC_LOGGER.error("Application startup failed.", e);
      connector.stop();
      context.close();
      throw e;
    }
  }
}
