package com.coral.oxygen.middleware.common.imdg

import com.coral.oxygen.middleware.common.configuration.DistributedInstanceConfiguration
import com.coral.oxygen.middleware.common.configuration.RedisConfiguration
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.test.context.ContextConfiguration
import org.springframework.test.context.TestPropertySource
import redis.embedded.RedisServer
import spock.lang.Shared
import spock.lang.Specification

@ContextConfiguration(classes = [DistributedInstanceConfiguration.class, RedisConfiguration.class])
@TestPropertySource(properties = ["imdg.ttl.seconds=200", "spring.redis.host = localhost", "spring.redis.port = 8083", "redisson.redis.sentinel.mode=false" ,"distributed.prefix = local"])
abstract class AbstractRedisDistributedInstanceSpec extends Specification {

  @Shared
  static DEFAULT_TESTING_REDIS_PORT = 8083

  @Autowired
  DistributedInstance distributedInstance

  @Shared
  static RedisServer testRedisServer

  def setupSpec() {
    testRedisServer = new RedisServer(DEFAULT_TESTING_REDIS_PORT)
    try {
      testRedisServer.start()
    }
    catch (IOException ex) {
      throw new IllegalStateException("Failed to start embedded Redis. " + ex.getMessage(), ex)
    }
  }

  def cleanupSpec() {
    if (testRedisServer != null) {
      testRedisServer.stop()
    }
  }
}
