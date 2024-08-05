package com.ladbrokescoral.aggregation.service;

import java.util.List;
import reactor.core.publisher.Mono;

public interface AggregationService {

  Mono<byte[]> imageAggregationByProvider(
      List<String> silkIds, String imageProvider, String requestId);

  Mono<byte[]> imageAggregationByBrand(List<String> eventIds, String brand, String requestId);
}
