package com.ladbrokescoral.cashout.repository;

import reactor.core.publisher.Mono;

public interface ReactiveLockRepository<T> {
  Mono<T> saveLock(String key, T value);

  Mono<T> getLock(String key);

  Mono<Boolean> deleteLock(String key);
}
