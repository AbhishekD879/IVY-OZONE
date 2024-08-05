package com.ladbrokescoral.reactions.repository.redis;

import static com.ladbrokescoral.reactions.util.ReactionHelper.getGlobalIncrementOrDecrementReactionKey;

import com.ladbrokescoral.reactions.dto.UserReactionDTO;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 16-06-2023
 */
@Repository
public class DefaultRedisReactionRepository implements RedisReactionRepository {

  private final RedisOperations redisOperations;
  private final RedisLongOperations redisLongOperations;

  public DefaultRedisReactionRepository(
      final RedisOperations redisOperations, final RedisLongOperations redisLongOperations) {

    this.redisOperations = redisOperations;
    this.redisLongOperations = redisLongOperations;
  }

  @Override
  public Mono<Long> saveReaction(
      final String userReactionKey,
      final String globalIncrementReactionKey,
      final String reactionId) {

    return redisOperations
        .set(userReactionKey, reactionId)
        .flatMap(result -> redisOperations.get(globalIncrementReactionKey))
        .flatMap(response -> redisOperations.increment(globalIncrementReactionKey))
        .switchIfEmpty(redisOperations.increment(globalIncrementReactionKey));
  }

  @Override
  public Mono<Long> updateReaction(
      final UserReactionDTO userReactionDTO,
      final String userReactionKey,
      final String incrementReactionKey,
      final String newReaction) {

    return redisOperations
        .getAndSet(userReactionKey, newReaction)
        .flatMap(
            oldReaction ->
                redisOperations.decrement(
                    getGlobalIncrementOrDecrementReactionKey(
                        userReactionDTO, Optional.of(oldReaction))))
        .flatMap(decrementCount -> redisOperations.increment(incrementReactionKey));
  }

  @Override
  public Mono<List<String>> getReactions(final List<String> keys) {

    return redisOperations.multiGet(keys);
  }

  @Override
  public Mono<Boolean> saveMongoUserDataIntoRedis(final Map<String, String> userKeys) {

    return redisOperations.multiSet(userKeys);
  }

  @Override
  public Mono<Boolean> saveMongoGlobalCountDataIntoRedis(final Map<String, Long> globalCountKeys) {

    return redisLongOperations.multiSet(globalCountKeys);
  }
}
