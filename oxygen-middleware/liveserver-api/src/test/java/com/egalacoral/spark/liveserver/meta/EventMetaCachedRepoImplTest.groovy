package com.egalacoral.spark.liveserver.meta

import com.github.benmanes.caffeine.cache.Cache
import com.github.benmanes.caffeine.cache.Caffeine
import spock.lang.Specification

class EventMetaCachedRepoImplTest extends Specification {
  private Cache cacheMock = Mock(Cache)
  private EventMetaCachedRepoImpl repo = new EventMetaCachedRepoImpl(cacheMock)

  def "testPutByEventId"() {
    when:
    repo.putByEventId(123, 16)
    then:
    interaction {
      verifyCachedByEventAndCategory(123, 16)
    }
  }

  def "test put by event Id with dto"() {
    when:
    repo.putByEventId(123, eventMeta(123, 16))
    then:
    interaction {
      verifyCachedByEventAndCategory(123, 16)
    }
  }

  def "test put by selectionId"() {
    when:
    repo.putBySelectionId(333, 123)
    then:
    interaction {
      verifyCachedEventById(333, 123)
    }
  }

  def "put by selectionId and dto"() {
    when:
    repo.putBySelectionId(333, EventMetaInfo.builder()
        .eventId(123)
        .build())
    then:
    interaction {
      verifyCachedEventById(333, 123)
    }
  }

  def "test put by market id"() {
    when:
    repo.putByMarketId(444, 123)
    then:
    interaction {
      verifyCachedEventById(444, 123)
    }
  }

  def "test put by market id and dto"() {
    when:
    repo.putByMarketId(444, EventMetaInfo.builder()
        .eventId(123)
        .build())
    then:
    interaction {
      verifyCachedEventById(444, 123)
    }
  }

  def "test get by eventId"() {
    when:
    repo.getByEventId(123)
    then:
    1 * cacheMock.getIfPresent(123)
  }

  def "test get bt market id"() {
    when:
    repo.getByMarketId(123)
    then:
    1 * cacheMock.getIfPresent(123)
  }

  def "test get by selection id"() {
    when:
    repo.getBySelectionId(123)
    then:
    1 * cacheMock.getIfPresent(123)
  }

  private EventMetaInfo eventMeta(Integer eventId) {
    EventMetaInfo.builder()
        .eventId(eventId)
        .build()
  }

  private EventMetaInfo eventMeta(Integer eventId, Integer categoryId) {
    EventMetaInfo.builder()
        .eventId(eventId)
        .categoryId(categoryId)
        .build()
  }

  private void verifyCachedEventById(int cacheKey, int eventId) {
    1 * cacheMock.put(cacheKey, EventMetaInfo.builder()
        .eventId(eventId)
        .build())
  }

  private void verifyCachedByEventAndCategory(Integer eventId, Integer categoryId) {
    1 * cacheMock.put(eventId, EventMetaInfo.builder()
        .eventId(eventId)
        .categoryId(categoryId)
        .build())
  }

}
