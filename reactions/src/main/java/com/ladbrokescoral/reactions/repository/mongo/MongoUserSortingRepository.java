package com.ladbrokescoral.reactions.repository.mongo;

import com.ladbrokescoral.reactions.repository.mongo.entity.MongoUserEntity;
import org.springframework.data.domain.Pageable;
import org.springframework.data.repository.reactive.ReactiveSortingRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;

/**
 * @author PBalarangakumar 07-09-2023
 */
@Repository
public interface MongoUserSortingRepository
    extends ReactiveSortingRepository<MongoUserEntity, String> {

  Flux<MongoUserEntity> findAllBy(Pageable pageable);
}
