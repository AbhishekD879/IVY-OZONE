package com.entain.oxygen;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.scheduling.annotation.EnableScheduling;
import reactor.tools.agent.ReactorDebugAgent;

@SpringBootApplication
@EnableScheduling
@EnableCaching
public class Application {

  public static void main(String[] args) {
    // debug hook to get more error details
    ReactorDebugAgent.init();

    SpringApplication.run(Application.class, args);
  }
}
