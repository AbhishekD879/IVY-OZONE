package com.ladbrokescoral.oxygen.betpackmp.service;

import java.util.List;
import reactor.core.publisher.Mono;

public interface CmsService {
  Mono<List<String>> getActiveBetPackIds(String brand);
}
