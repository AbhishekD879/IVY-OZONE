package com.coral.oxygen.middleware.common.imdg

import com.coral.oxygen.middleware.common.configuration.DistributedKey
import org.springframework.boot.actuate.health.HealthIndicator

class RedisDistributedInstanceSpec extends AbstractRedisDistributedInstanceSpec {

  def "Test Distributed map"() {
    given:
    def testMap = distributedInstance.getMap(DistributedKey.ERRORS_MAP)
    testMap.put("key", "value")
    def expectedValue = distributedInstance.getMap(DistributedKey.ERRORS_MAP).get("key")
    expect:
    "value" == expectedValue
  }
  def "Test atomic long"() {
    given:
    def atomicLong = distributedInstance.getAtomicLong(DistributedKey.ATOMIC_FEATURED_DATA)
    def actual = atomicLong.addAndGet(1L)
    expect:
    actual == atomicLong.get()
  }

  def "Test provideName"() {
    when:
    String providerName = distributedInstance.providerName
    then:
    providerName == "redis_template"
  }

  def "Test healthIndicator"() {
    when:
    HealthIndicator healthIndicator = distributedInstance.getHealthIndicator()
    then:
    healthIndicator != null
  }


  def "Test getValueMethod"() {
    when:
    distributedInstance.updateExpirableValue(DistributedKey.LAST_RUN_TIME,"1662186412");
    String result = distributedInstance.getValue(DistributedKey.LAST_RUN_TIME)
    then:
    "1662186412" == result
  }

  def "Test getKeyValuesMethod"() {
    List<String> ls=new ArrayList<>()
    ls.add("prefix1")
    when:
    List<String> result = distributedInstance.getValues(DistributedKey.ERRORS_MAP,ls)
    then:
    result.size()==1
  }
}
