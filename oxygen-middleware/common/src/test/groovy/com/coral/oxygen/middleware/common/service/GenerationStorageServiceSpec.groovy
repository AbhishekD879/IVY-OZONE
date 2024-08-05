package com.coral.oxygen.middleware.common.service

import com.coral.oxygen.middleware.common.configuration.DistributedKey
import com.coral.oxygen.middleware.common.imdg.AbstractRedisDistributedInstanceSpec

class GenerationStorageServiceSpec extends AbstractRedisDistributedInstanceSpec {

  final String GENERATION_VALUE_FEATURED = 'featuredGen'
  final String GENERATION_VALUE_INPLAY = 'inplayGen'

  GenerationStorageService service

  def "Put latest generation to distributedMap"() {
    given:
    service = new GenerationStorageService(distributedInstance)
    when:
    service.putLatest(GenerationKeyType.FEATURED_GENERATION, GENERATION_VALUE_FEATURED)
    String result = distributedInstance.getValue(DistributedKey.GENERATION_MAP, GenerationKeyType.FEATURED_GENERATION.key)
    then:
    result == GENERATION_VALUE_FEATURED
  }
  def "Get latest generation to distributedMap"() {
    given:
    service = new GenerationStorageService(distributedInstance)
    distributedInstance.updateExpirableValue(DistributedKey.GENERATION_MAP, GenerationKeyType.INPLAY_GENERATION.getKey(), GENERATION_VALUE_INPLAY)
    when:
    String latestValue = service.getLatest(GenerationKeyType.INPLAY_GENERATION)
    then:
    latestValue == GENERATION_VALUE_INPLAY
  }
}
