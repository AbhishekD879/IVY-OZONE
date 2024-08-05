package com.entain.oxygen.betbuilder_middleware.service;

import com.entain.oxygen.betbuilder_middleware.api.request.PriceRequest;
import com.entain.oxygen.betbuilder_middleware.api.response.Price;
import com.entain.oxygen.betbuilder_middleware.api.response.PriceResponse;
import com.entain.oxygen.betbuilder_middleware.redis.dto.CombinationCache;
import com.entain.oxygen.betbuilder_middleware.repository.RedissonCombinationRepository;
import com.entain.oxygen.betbuilder_middleware.repository.RedissonEventIdRepository;
import com.entain.oxygen.betbuilder_middleware.service.helper.CacheServiceHelper;
import java.util.*;
import java.util.stream.Collectors;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

@Service
public class CacheService {
  private final RedissonCombinationRepository combinationRedisRepository;
  private final RedissonEventIdRepository eventIdRepository;
  private final CacheServiceHelper cacheServiceHelper;

  @Autowired
  public CacheService(
      RedissonCombinationRepository combinationRedisRepository,
      RedissonEventIdRepository eventIdRepository,
      CacheServiceHelper cacheServiceHelper) {
    this.combinationRedisRepository = combinationRedisRepository;
    this.eventIdRepository = eventIdRepository;
    this.cacheServiceHelper = cacheServiceHelper;
  }

  public void cacheCombinationData(PriceRequest request, PriceResponse response) {
    Mono.fromRunnable(
            () -> {
              Map<String, String> combinationIdSgpIdMap =
                  response.getPrices().stream()
                      .filter(price -> StringUtils.isNotBlank(price.getSgpId()))
                      .collect(Collectors.toMap(Price::getCombinationId, Price::getSgpId));

              Map<String, CombinationCache> mapToSave =
                  request.getCombinations().stream()
                      .filter(combination -> combinationIdSgpIdMap.containsKey(combination.getId()))
                      .map(
                          combination ->
                              cacheServiceHelper.buildCombinationCache(
                                  combination, combinationIdSgpIdMap.get(combination.getId())))
                      .collect(Collectors.toMap(CombinationCache::getHash, c -> c));
              combinationRedisRepository.saveCombinations(mapToSave);
            })
        .subscribeOn(Schedulers.boundedElastic())
        .subscribe();
  }

  public void cacheEventMapping(PriceRequest request, PriceResponse response) {
    Mono.fromRunnable(
            () -> {
              Map<String, String> mapToSave = new HashMap<>();
              response
                  .getPrices()
                  .forEach(
                      (Price price) ->
                          request.getCombinations().stream()
                              .filter(
                                  combination ->
                                      price.getCombinationId().equals(combination.getId())
                                          && !StringUtils.isEmpty(combination.getOEId())
                                          && !StringUtils.isEmpty(price.getSgpId()))
                              .forEach(
                                  combination ->
                                      mapToSave.put(
                                          combination.getOEId(),
                                          combination.getSelections().get(0).getFixtureId())));

              eventIdRepository.saveEvents(mapToSave);
            })
        .subscribeOn(Schedulers.boundedElastic())
        .subscribe();
  }

  public Mono<Map<String, CombinationCache>> getCombinations(Set<String> keys) {
    return combinationRedisRepository.getCombinations(keys);
  }

  /**
   * This method accepts the combinations from the request and returns all the hashes in the request
   * as a set which would be the input to the redis
   */
}
