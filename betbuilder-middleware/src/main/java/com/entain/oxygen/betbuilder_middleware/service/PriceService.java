package com.entain.oxygen.betbuilder_middleware.service;

import com.entain.oxygen.betbuilder_middleware.api.request.CheckPriceRequest;
import com.entain.oxygen.betbuilder_middleware.api.request.Combinations;
import com.entain.oxygen.betbuilder_middleware.api.request.PriceRequest;
import com.entain.oxygen.betbuilder_middleware.api.response.CheckPriceResponse;
import com.entain.oxygen.betbuilder_middleware.api.response.PriceResponse;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.jboss.logging.MDC;
import org.redisson.client.RedisException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

@Service
public class PriceService {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger();
  private final BPGService bpgService;
  private final CacheService cacheService;

  @Autowired
  public PriceService(BPGService bpgService, CacheService cacheService) {
    this.bpgService = bpgService;
    this.cacheService = cacheService;
  }

  public Mono<PriceResponse> getPrice(PriceRequest request) {
    return bpgService
        .getPrice(request)
        .doOnNext(response -> cacheService.cacheCombinationData(request, response))
        .doOnNext(response -> cacheService.cacheEventMapping(request, response))
        .subscribeOn(Schedulers.parallel());
  }

  public Mono<CheckPriceResponse> getLatestPrices(CheckPriceRequest request) {
    String correlationId = (String) MDC.get(BBUtil.CORRELATION_ID);
    return cacheService
        .getCombinations(extractHashIds(request.getCombinations()))
        .flatMap(bpgService.getLatestPrices(request, correlationId))
        .onErrorResume(
            (Throwable error) -> {
              ASYNC_LOGGER.error("Error - {}", error.getMessage());
              if (error instanceof RedisException) {
                return Mono.error(new RedisException("Redis Technical Error Occured"));
              } else {
                return Mono.error(error);
              }
            });
  }

  private Set<String> extractHashIds(List<Combinations> combinations) {
    return combinations.stream().map(Combinations::getBbHash).collect(Collectors.toSet());
  }
}
