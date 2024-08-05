package com.ladbrokescoral.reactions.service;

import com.ladbrokescoral.reactions.dto.GlobalCount;
import com.ladbrokescoral.reactions.repository.mongo.entity.MongoUserEntity;
import java.util.List;
import java.util.Map;
import org.springframework.data.domain.Pageable;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 14-06-2023
 */
public interface MongoReactionService {

  Mono<MongoUserEntity> saveUser(MongoUserEntity userEntity);

  Mono<MongoUserEntity> updateUser(MongoUserEntity userEntity);

  Flux<String> getAllUserDeleteKeys();

  Mono<Void> deleteUsers(List<String> deleteKeys);

  Flux<GlobalCount> getReactionGlobalCount();

  Mono<Long> getUsersCount();

  Mono<Map<String, String>> findAllPaginatedUsers(Pageable pageable);
}
