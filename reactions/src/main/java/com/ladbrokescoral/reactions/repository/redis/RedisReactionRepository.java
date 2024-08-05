package com.ladbrokescoral.reactions.repository.redis;

import com.ladbrokescoral.reactions.dto.UserReactionDTO;
import java.util.List;
import java.util.Map;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 16-06-2023
 */
public interface RedisReactionRepository {

  Mono<Long> saveReaction(
      String userReactionKey, String globalIncrementReactionKey, String reactionId);

  Mono<Long> updateReaction(
      UserReactionDTO userReactionDTO,
      String userReactionKey,
      String incrementReactionKey,
      String newReaction);

  Mono<List<String>> getReactions(List<String> keys);

  Mono<Boolean> saveMongoUserDataIntoRedis(Map<String, String> userKeys);

  Mono<Boolean> saveMongoGlobalCountDataIntoRedis(Map<String, Long> globalCountKeys);
}
