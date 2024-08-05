package com.ladbrokescoral.oxygen.cms;

import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;

@Slf4j
@EnableEurekaClient
@EnableScheduling
@EnableCaching(proxyTargetClass = true)
@SpringBootApplication
@EnableAsync
public class Application {

  public static final String MONGOCK = "mongockInitializingBeanRunner";

  public static void main(String[] args) {
    SpringApplication.run(Application.class, args);
  }
}
