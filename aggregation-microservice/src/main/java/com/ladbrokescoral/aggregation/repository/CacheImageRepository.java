package com.ladbrokescoral.aggregation.repository;

import java.util.Collection;
import java.util.List;
import reactor.core.publisher.Mono;

public interface CacheImageRepository<K, T> {

  Mono<T> save(K key, T value);

  Mono<T> get(K key);

  Mono<List<T>> multiGet(Collection<K> keys);

  Mono<Boolean> delete(K key);
}
