package com.coral.oxygen.middleware;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.redis.repository.configuration.EnableRedisRepositories;
import org.springframework.integration.zookeeper.leader.LeaderInitiator;
import org.springframework.scheduling.annotation.EnableScheduling;

@EnableEurekaClient
@SpringBootApplication
@EnableScheduling
@EnableRedisRepositories
@ComponentScan({
  "com.coral.oxygen.middleware.*",
  "com.egalacoral.spark",
  "com.ladbrokescoral.lib.*"
})
@EnableCaching
public class Application {
  @Autowired
  public static void main(String[] args) {
    ConfigurableApplicationContext context = SpringApplication.run(Application.class, args);
    LeaderInitiator leaderInitiator = context.getBean(LeaderInitiator.class);
    leaderInitiator.setAutoStartup(true);
    leaderInitiator.start();
  }
}
