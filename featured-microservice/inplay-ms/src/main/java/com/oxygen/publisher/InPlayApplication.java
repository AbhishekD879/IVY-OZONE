package com.oxygen.publisher;

import com.newrelic.api.agent.NewRelic;
import com.oxygen.publisher.inplay.InplayServiceRegistry;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.ComponentScan;

@EnableEurekaClient
@SpringBootApplication
@ComponentScan(
    basePackages = {
      "com.oxygen.publisher.inplay.configuration",
      "com.oxygen.publisher.configuration",
      "com.oxygen.publisher.service",
      "com.oxygen.publisher.inplay.service",
      "com.oxygen.service.discovery.api",
      "com.oxygen.service.discovery.configuration",
      "com.oxygen.health.api"
    })
@Slf4j
public class InPlayApplication {

  public static void main(String[] args) {
    ConfigurableApplicationContext context = SpringApplication.run(InPlayApplication.class, args);
    InplayServiceRegistry inplayServiceRegistry = context.getBean(InplayServiceRegistry.class);
    try {
      inplayServiceRegistry.load();
      inplayServiceRegistry.getSocketIOServer().start();
    } catch (Exception e) {
      NewRelic.noticeError(e);
      log.error("InPlayApplication startup failed.", e);
      inplayServiceRegistry.stop();
      context.close();
      throw e;
    }
  }
}
