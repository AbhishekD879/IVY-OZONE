package com.ladbrokescoral.cashout.repository;

import java.util.Collection;
import java.util.List;
import reactor.core.publisher.Mono;

public interface ReactiveRepository<T> {
  Mono<Boolean> save(String selectionId, T value);

  Mono<Boolean> save(T value);

  Mono<T> get(String selectionId);

  Mono<List<T>> multiGet(Collection<String> selectionIds);

  Mono<Boolean> delete(String selectionId);
}
