package com.ladbrokescoral.reactions;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.mongodb.config.EnableMongoAuditing;
import org.springframework.data.mongodb.repository.config.EnableReactiveMongoRepositories;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * @author PBalarangakumar 12-06-2023
 */
@SuppressWarnings("java:S4604")
@SpringBootApplication
@EnableMongoAuditing
@EnableReactiveMongoRepositories
@EnableScheduling
public class ReactionsApplication {

  public static void main(String[] args) {
    SpringApplication.run(ReactionsApplication.class, args);
  }
}
