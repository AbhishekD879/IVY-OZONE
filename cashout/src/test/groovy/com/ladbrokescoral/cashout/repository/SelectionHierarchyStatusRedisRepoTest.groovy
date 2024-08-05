package com.ladbrokescoral.cashout.repository

import org.springframework.data.redis.core.ReactiveRedisTemplate
import org.springframework.data.redis.core.ReactiveValueOperations
import reactor.core.publisher.Mono
import reactor.test.StepVerifier
import spock.lang.Specification
import java.math.BigInteger;

class SelectionHierarchyStatusRedisRepoTest extends Specification {
  def repoMock = Mock(ReactiveRedisTemplate)
  def opsForValue = Mock(ReactiveValueOperations)
  def statusRepo = new SelectionHierarchyStatusRedisRepo(repoMock)

  void setup() {
    repoMock.opsForValue() >> opsForValue
  }

  def "Null responses from redis are filtered out"() {
    given:
    def entityStatus = new EntityStatus(BigInteger.valueOf(2), true)
    opsForValue.multiGet(_) >> Mono.just([null, entityStatus, null])
    when:
    def statuses = statusRepo.fetchMarketStatuses([
      BigInteger.valueOf(1),
      BigInteger.valueOf(2),
      BigInteger.valueOf(3)
    ])
    then:
    StepVerifier.create(statuses)
        .expectNext([entityStatus])
        .verifyComplete()
  }
}
