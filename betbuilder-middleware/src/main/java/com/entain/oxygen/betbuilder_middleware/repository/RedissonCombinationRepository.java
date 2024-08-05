package com.entain.oxygen.betbuilder_middleware.repository;

import com.entain.oxygen.betbuilder_middleware.redis.dto.CombinationCache;
import java.util.*;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.redisson.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;

@Repository
public class RedissonCombinationRepository {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger();
  private RedissonReactiveClient redissonReactiveClient;
  private final RLocalCachedMapReactive<String, CombinationCache> redissionCombinationEntities;
  private static final String COMBINATION_MAP = "COMBINATION_MAP";
  private static final String INDEX = "index:oEId:";

  @Autowired
  public RedissonCombinationRepository(RedissonReactiveClient redissonReactiveClient) {
    this.redissonReactiveClient = redissonReactiveClient;
    redissionCombinationEntities =
        redissonReactiveClient.getLocalCachedMap(COMBINATION_MAP, LocalCachedMapOptions.defaults());
  }

  public void saveCombinations(Map<String, CombinationCache> combinationCacheMap) {
    RBatchReactive batchReactive = redissonReactiveClient.createBatch();
    combinationCacheMap.forEach(
        (String hash, CombinationCache combinationCache) -> {
          batchReactive
              .getMap(COMBINATION_MAP)
              .fastPutIfAbsent(hash, combinationCache)
              .filter(isAbsent -> isAbsent)
              .doOnNext(
                  isAbsent ->
                      ASYNC_LOGGER.info(
                          "Saved combination with hash: {} and CombinationCache: {}",
                          hash,
                          combinationCache))
              .subscribe();
          batchReactive.getSet(INDEX + combinationCache.getOEId()).add(hash);
        });
    batchReactive
        .execute()
        .subscribe(
            batchResult ->
                ASYNC_LOGGER.debug(
                    "Save combination Batch response: {}", batchResult.getResponses()));
  }

  public Mono<Map<String, CombinationCache>> getCombinations(Set<String> keys) {
    return redissionCombinationEntities.getAll(keys);
  }

  public Mono<List<Object>> getCombinationsByOeId(String oEId) {
    return redissonReactiveClient.getSet(INDEX + oEId).iterator().collectList();
  }

  public void deleteCombinations(String oEId, List<Object> sgpIds) {
    List<String> sgpIdStrings = sgpIds.stream().map(Object::toString).toList();
    ASYNC_LOGGER.info(
        "{} sgpIds associated with eventId -> {} to delete from redis", sgpIds.size(), oEId);
    RBatchReactive batchReactive = redissonReactiveClient.createBatch();
    batchReactive.getSet(INDEX + oEId).delete();
    sgpIdStrings.forEach(sgpId -> batchReactive.getMap(COMBINATION_MAP).fastRemove(sgpId));

    batchReactive.execute().subscribe();
  }
}
