package com.oxygen.publisher.model

import groovy.util.logging.Slf4j
import spock.lang.Specification

@Slf4j
class InplayCachedDataSpec extends Specification {

  InplayCachedData inCache
  Thread writer
  Thread reader0
  Thread reader1
  Thread reader2
  Thread reader3
  Thread reader4
  Thread reader5
  static final int MODULE = EventType.values().length * 10

  def setup() {
    inCache = new InplayCachedData()
    inCache.addLiveUpdatesCache(createBaseObject(EventType.EVMKT.toString(), 1, 1001))
    inCache.addLiveUpdatesCache(createBaseObject(EventType.EVMKT.toString(), 1, 1002))
    inCache.addLiveUpdatesCache(createBaseObject(EventType.EVMKT.toString(), 2, 2001))
    inCache.addLiveUpdatesCache(createBaseObject(EventType.EVMKT.toString(), 2, 2002))
    writer = new Thread(writeRunner)
    reader0 = new Thread(readRunner)
    reader1 = new Thread(readRunner)
    reader2 = new Thread(readRunner)
    reader3 = new Thread(readRunner)
    reader4 = new Thread(readRunner)
    reader5 = new Thread(readRunner)
  }


  def "Get live Update Cache"() {
    setup:
    writer.start()
    reader0.start()
    reader1.start()
    reader2.start()
    reader3.start()
    reader4.start()
    reader5.start()
    long timer = System.currentTimeMillis()
    while (writer.isAlive() || reader0.isAlive() || reader1.isAlive() || reader2.isAlive() || reader3.isAlive() || reader4.isAlive() || reader5.isAlive()) {
      Thread.sleep(1)
      log.info("Writer: " + writer.isAlive() + " Reader0:" + reader0.isAlive() + " Reader1:" + reader1.isAlive())
    }
    long result = System.currentTimeMillis() - timer
    log.info("time:" + result)

    expect:
    !writer.isAlive() && !reader0.isAlive() && !reader1.isAlive() && !reader2.isAlive() && !reader3.isAlive() && !reader4.isAlive() && !reader5.isAlive()
    62 == inCache.getPayload("1").length
    62 == inCache.getPayload("2").length
  }

  //------------helpers---------------

  enum EventType {
    PRICE,
    EVMKT,
    SELCN,
    EVENT,
    SCBRD,
    CLOCK
  }

  Runnable readRunner = new Runnable() {
    @Override
    void run() {
      for (int i = 0; i < 2000; i++) {
        BaseObject[] payload = inCache.getPayload("1")
        for (BaseObject bo : payload) {
          try {
            json.toJson(bo)
          } catch (Exception ignored) {
          }
        }
      }
    }
  }

  Runnable writeRunner = new Runnable() {
    @Override
    void run() {
      for (int i = 0; i < 10000; i++) {
        if (Math.random() > 0.5) {
          inCache.addLiveUpdatesCache(createBaseObject(EventType.EVMKT.toString(), 1, Math.floorMod(i, MODULE)))
        } else {
          inCache.addLiveUpdatesCache(createBaseObject(EventType.EVMKT.toString(), 2, Math.floorMod(i, MODULE)))
        }
      }
    }
  }


  BaseObject createBaseObject(String typeName, int id, int marketId) {
    return BaseObject.builder()
        .type(typeName)
        .event(BaseObject.Event.builder()
        .eventId(id)
        .market(BaseObject.Market.builder()
        .marketId(marketId)
        .outcome(BaseObject.Outcome.builder()
        .outcomeId(id)
        .build())
        .build())
        .build())
        .build()
  }
}
