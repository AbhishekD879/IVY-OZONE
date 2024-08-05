package com.ladbrokescoral.aggregation.service;

import com.ladbrokescoral.aggregation.model.SilkUrl;
import java.util.List;
import reactor.core.publisher.Mono;

public interface SilkUrlProviderService {

  Mono<List<SilkUrl>> getSilksUrlsByEventIds(String brand, List<String> eventIds);
}
