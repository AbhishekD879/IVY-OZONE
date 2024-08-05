package com.ladbrokescoral.cashout.service

import com.ladbrokescoral.cashout.EmbededRedis
import com.ladbrokescoral.cashout.config.RedisConfig
import com.ladbrokescoral.cashout.model.RedisSaverLock
import com.ladbrokescoral.cashout.repository.LockRepository
import com.ladbrokescoral.cashout.repository.ReactiveLockRepository
import com.ladbrokescoral.cashout.service.masterslave.MasterSlaveService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.autoconfigure.cache.CacheAutoConfiguration
import org.springframework.boot.test.autoconfigure.data.redis.DataRedisTest
import org.springframework.context.annotation.Import
import org.springframework.test.annotation.DirtiesContext
import org.springframework.test.context.ActiveProfiles
import spock.lang.Specification

@Import([EmbededRedis, RedisConfig, MasterSlaveService, LockRepository])
@DataRedisTest(excludeAutoConfiguration = [CacheAutoConfiguration])
@ActiveProfiles("UNIT")
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
class MasterSlaveServiceTest extends Specification {
  @Autowired
  ReactiveLockRepository<RedisSaverLock> lockRepository
  def changeMasterTimeAfter = 1000

  def "Test lock is setted"() {
    given:
    def service1 = new MasterSlaveService(changeMasterTimeAfter, lockRepository)
    def service2 = new MasterSlaveService(changeMasterTimeAfter, lockRepository)
    when:
    service1.process()
    Thread.sleep(500)
    service2.process()

    then:
    service1.isMaster()
    !service2.isMaster()
  }

  def "Lock is changed after timeout"() {
    given:
    def service1 = new MasterSlaveService(changeMasterTimeAfter, lockRepository)
    def service2 = new MasterSlaveService(changeMasterTimeAfter, lockRepository)
    when:
    service1.process()
    Thread.sleep(1500)
    service2.process()
    Thread.sleep(500)
    service1.process()
    Thread.sleep(100)

    then:
    !service1.isMaster()
    service2.isMaster()
  }
}
