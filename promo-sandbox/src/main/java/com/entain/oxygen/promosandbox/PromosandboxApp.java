package com.entain.oxygen.promosandbox;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.actuate.autoconfigure.endpoint.jmx.JmxEndpointAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication(exclude = {JmxEndpointAutoConfiguration.class})
@EnableScheduling
@EnableCaching
public class PromosandboxApp {

  public static void main(String[] args) {
    SpringApplication.run(PromosandboxApp.class, args);
  }
}
