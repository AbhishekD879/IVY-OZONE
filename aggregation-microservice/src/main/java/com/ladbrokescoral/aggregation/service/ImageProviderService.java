package com.ladbrokescoral.aggregation.service;

import com.ladbrokescoral.aggregation.model.ImageData;
import com.ladbrokescoral.aggregation.model.SilkUrl;
import reactor.core.publisher.Mono;

public interface ImageProviderService {
  Mono<ImageData> getImage(SilkUrl silkUrl);
}
