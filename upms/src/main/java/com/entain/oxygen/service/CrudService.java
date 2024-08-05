package com.entain.oxygen.service;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public interface CrudService<E> {

  <S extends E> Mono<E> save(S entity);

  Flux<E> findAll();
}
