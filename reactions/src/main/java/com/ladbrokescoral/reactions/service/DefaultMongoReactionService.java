package com.ladbrokescoral.reactions.service;

import com.ladbrokescoral.reactions.dto.GlobalCount;
import com.ladbrokescoral.reactions.repository.mongo.MongoUserRepository;
import com.ladbrokescoral.reactions.repository.mongo.MongoUserSortingRepository;
import com.ladbrokescoral.reactions.repository.mongo.entity.MongoUserEntity;
import java.util.List;
import java.util.Map;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 14-06-2023
 */
@Component
public class DefaultMongoReactionService implements MongoReactionService {

  private final MongoUserRepository userRepository;
  private final MongoUserSortingRepository sortingRepository;

  public DefaultMongoReactionService(
      final MongoUserRepository userRepository,
      final MongoUserSortingRepository sortingRepository) {

    this.userRepository = userRepository;
    this.sortingRepository = sortingRepository;
  }

  @Override
  public Mono<MongoUserEntity> saveUser(final MongoUserEntity userEntity) {
    return userRepository.save(userEntity);
  }

  @Override
  public Mono<MongoUserEntity> updateUser(final MongoUserEntity userEntity) {

    return userRepository
        .findById(userEntity.redisKey())
        .flatMap(dbEntity -> userRepository.save(userEntity));
  }

  @Override
  public Flux<String> getAllUserDeleteKeys() {

    return userRepository.findAll().map(MongoUserEntity::deleteKey).distinct();
  }

  @Override
  public Mono<Void> deleteUsers(final List<String> deleteKeys) {

    return userRepository.deleteAllByDeleteKeys(deleteKeys);
  }

  @Override
  public Flux<GlobalCount> getReactionGlobalCount() {

    return userRepository.getReactionGlobalCount();
  }

  @Override
  public Mono<Long> getUsersCount() {

    return userRepository.getUsersCount();
  }

  @Override
  public Mono<Map<String, String>> findAllPaginatedUsers(Pageable pageable) {

    return sortingRepository
        .findAllBy(pageable)
        .collectMap(MongoUserEntity::redisKey, MongoUserEntity::redisValue);
  }
}
