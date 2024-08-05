package com.coral.oxygen.middleware.common.imdg

import com.coral.oxygen.middleware.common.configuration.RedisConfiguration
import com.coral.oxygen.middleware.common.exceptions.InvalidConfigurationException
import org.redisson.config.Config
import org.springframework.test.context.TestPropertySource
import spock.lang.Specification

@TestPropertySource(properties = ["imdg.ttl.seconds=200", "redisson.redis.sentinel.master = testmaster", "redisson.redis.sentinel.nodes = redis://localhost:8083", "redisson.redis.sentinel.mode=true"])
class AbstractSenetelRedisDistributedInstanceSpec extends Specification {



  def "Test Sentinel Server with nodes"() {
    given:
    RedisConfiguration redissonConfigProvider = new RedisConfiguration();
    Config config = redissonConfigProvider.getSentinelServerConfig("testmaster","redis://localhost:8083","password",false);
    expect:
    true == config.isSentinelConfig()
  }

  def "Test Sentinel Server with nodes without password"() {
    given:
    RedisConfiguration redissonConfigProvider = new RedisConfiguration();
    Config config = redissonConfigProvider.getSentinelServerConfig("testmaster","redis://localhost:8083","", true);
    expect:
    true == config.isSentinelConfig()
  }

  def "Test Sentinel Server with no nodes"() {
    when:
    RedisConfiguration redissonConfigProvider = new RedisConfiguration();
    Config config = redissonConfigProvider.getSentinelServerConfig("testmaster","","",false);
    then:
    final InvalidConfigurationException exception = thrown()
    exception.message == 'Please provide redis sentinel servers in property REDIS_SENTINEL_SERVERS'
  }
}
