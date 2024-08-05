package com.entain.oxygen.repository;

import org.springframework.data.mongodb.repository.ReactiveMongoRepository;
import org.springframework.data.repository.NoRepositoryBean;
import reactor.core.publisher.Flux;

@NoRepositoryBean
public interface BaseRepository<E> extends ReactiveMongoRepository<E, String> {

  Flux<E> findByBrand(String brand);
}
