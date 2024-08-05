package com.entain.oxygen.repository;

import com.entain.oxygen.entity.UserStable;
import org.springframework.data.mongodb.repository.Aggregation;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;

@Repository
public interface UserStableRepository extends BaseRepository<UserStable> {

  Mono<UserStable> findByUserName(String userName);

  @Query(value = "{ 'userName' : ?0 }", fields = "{ 'myStable.note' : 0}")
  Mono<UserStable> findByUserNameAndBrandExcludingNotes(String userName);

  @Aggregation({
    "{$match: {userName: ?0, 'myStable.horseId': ?1}}",
    "{$project: {myStable: {$filter: {input: '$myStable', as: 'horse', cond: {$eq: ['$$horse.horseId', ?1]}}}}}"
  })
  Mono<UserStable> getNotesByHorseId(String userName, String horseId);
}
