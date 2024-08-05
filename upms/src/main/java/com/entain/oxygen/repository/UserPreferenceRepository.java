package com.entain.oxygen.repository;

import com.entain.oxygen.entity.UserPreference;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public interface UserPreferenceRepository extends BaseRepository<UserPreference> {

  Mono<UserPreference> findByUserNameAndBrand(String userName, String brand);

  Flux<UserPreference> findAllByBrand(String brand);
}
