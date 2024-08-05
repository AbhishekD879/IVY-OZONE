package com.ladbrokescoral.oxygen.betpackmp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.web.servlet.MultipartAutoConfiguration;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.redis.repository.configuration.EnableRedisRepositories;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication(exclude = {MultipartAutoConfiguration.class})
@EnableRedisRepositories
@ComponentScan("com.ladbrokescoral.oxygen.betpackmp")
@EnableScheduling
public class BetPackMpApplication {

  public static void main(String[] args) {
    SpringApplication.run(BetPackMpApplication.class, args);
  }
}
