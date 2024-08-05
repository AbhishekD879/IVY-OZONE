package com.ladbrokescoral.oxygen.trendingbets;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.web.reactive.config.EnableWebFlux;
import reactor.tools.agent.ReactorDebugAgent;

@EnableWebFlux
@SpringBootApplication
@EnableConfigurationProperties
public class Application {

  public static void main(String[] args) {
    // debug hook to get more error details
    ReactorDebugAgent.init();
    SpringApplication.run(Application.class, args);
  }
}
