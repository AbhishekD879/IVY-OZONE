package com.entain.oxygen.service;

import com.entain.oxygen.repository.BaseRepository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public class AbstractService<E> implements CrudService<E> {

  protected BaseRepository<E> baseRepository;

  public AbstractService(BaseRepository<E> baseRepository) {
    this.baseRepository = baseRepository;
  }

  @Override
  public <S extends E> Mono<E> save(S entity) {
    return baseRepository.save(entity);
  }

  @Override
  public Flux<E> findAll() {
    return baseRepository.findAll();
  }
}
