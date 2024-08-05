package com.ladbrokescoral.reactions.repository.mongo;

import com.ladbrokescoral.reactions.dto.GlobalCount;
import com.ladbrokescoral.reactions.repository.mongo.entity.MongoUserEntity;
import java.util.List;
import org.springframework.data.mongodb.repository.Aggregation;
import org.springframework.data.mongodb.repository.DeleteQuery;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.data.mongodb.repository.ReactiveMongoRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 17-06-2023
 */
@Repository
public interface MongoUserRepository extends ReactiveMongoRepository<MongoUserEntity, String> {

  @Aggregation(
      pipeline =
          "{'$group' : {_id:{deleteKey:'$deleteKey',redisValue:'$redisValue'}, count:{$sum:1}}}")
  Flux<GlobalCount> getReactionGlobalCount();

  @DeleteQuery(value = "{'deleteKey': {$in : ?0}}")
  Mono<Void> deleteAllByDeleteKeys(List<String> deleteKeys);

  @Query(value = "{ '_id' : { $exists : true }}", count = true)
  Mono<Long> getUsersCount();
}
