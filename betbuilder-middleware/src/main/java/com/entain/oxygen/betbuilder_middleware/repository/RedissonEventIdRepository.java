package com.entain.oxygen.betbuilder_middleware.repository;

import java.util.Map;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.redisson.api.LocalCachedMapOptions;
import org.redisson.api.RBatchReactive;
import org.redisson.api.RLocalCachedMapReactive;
import org.redisson.api.RedissonReactiveClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;

@Repository
public class RedissonEventIdRepository {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger();
  private final RLocalCachedMapReactive<String, String> redissionEventId;
  private final RedissonReactiveClient redissonReactiveClient;

  @Autowired
  public RedissonEventIdRepository(RedissonReactiveClient redissonReactiveClient) {
    this.redissonReactiveClient = redissonReactiveClient;
    redissionEventId =
        redissonReactiveClient.getLocalCachedMap("EventIDs_MAP", LocalCachedMapOptions.defaults());
  }

  public Mono<Map<String, String>> readEvents() {
    return redissionEventId.readAllMap();
  }

  public void saveEvents(Map<String, String> eventCacheMap) {
    RBatchReactive batchReactive = redissonReactiveClient.createBatch();
    eventCacheMap.forEach(
        (String oeId, String beId) ->
            batchReactive
                .getMap("EventIDs_MAP")
                .fastPutIfAbsent(oeId, beId)
                .filter(isAbsent -> isAbsent)
                .doOnNext(
                    isAbsent ->
                        ASYNC_LOGGER.info("Saved event with oeId: {} and beId: {}", oeId, beId))
                .subscribe());
    batchReactive
        .execute()
        .subscribe(
            batchResult ->
                ASYNC_LOGGER.debug(
                    "Save EventId Map Batch response: {}", batchResult.getResponses()));
  }

  public Mono<Boolean> delete(String key) {
    return redissionEventId.fastRemove(key).hasElement();
  }
}
