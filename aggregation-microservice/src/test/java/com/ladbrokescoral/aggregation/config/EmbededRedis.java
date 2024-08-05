package com.ladbrokescoral.aggregation.config;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import org.springframework.boot.autoconfigure.data.redis.RedisProperties;
import org.springframework.boot.test.context.TestConfiguration;
import redis.embedded.RedisServer;

@TestConfiguration
public class EmbededRedis {

  private RedisServer redisServer;

  public EmbededRedis(RedisProperties redisProperties) {
    this.redisServer = new RedisServer(redisProperties.getPort());
  }

  @PostConstruct
  public void postConstruct() {
    redisServer.start();
  }

  @PreDestroy
  public void preDestroy() {
    redisServer.stop();
  }
}
