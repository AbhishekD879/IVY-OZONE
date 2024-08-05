package com.ladbrokescoral.oxygen.buildyourbetms;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;
import org.springframework.web.reactive.config.EnableWebFlux;

@EnableEurekaClient
@SpringBootApplication
@EnableWebFlux
public class BuildYourBetMsApplication {

  public static void main(String[] args) {
    SpringApplication.run(BuildYourBetMsApplication.class, args);
  }
}
