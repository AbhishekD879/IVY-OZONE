package com.ladbrokescoral.reactions.repository;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.reactions.dto.ErrorDTO;
import com.ladbrokescoral.reactions.dto.Reaction;
import com.ladbrokescoral.reactions.dto.UserReactionDTO;
import com.ladbrokescoral.reactions.exception.BadRequestException;
import com.ladbrokescoral.reactions.exception.ErrorCode;
import com.ladbrokescoral.reactions.repository.redis.DefaultRedisReactionRepository;
import com.ladbrokescoral.reactions.repository.redis.RedisLongOperations;
import com.ladbrokescoral.reactions.repository.redis.RedisOperations;
import java.time.OffsetDateTime;
import java.util.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.*;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

class DefaultRedisReactionRepositoryTest {

  @InjectMocks private DefaultRedisReactionRepository redisReactionRepository;

  @Mock private RedisOperations redisOperations;

  @Mock private RedisLongOperations redisLongOperations;

  @BeforeEach
  void setUp() {
    MockitoAnnotations.initMocks(this);
  }

  @Test
  void testSaveReaction() {
    String userReactionKey = "user:123:reaction";
    String globalIncrementReactionKey = "global:reaction:count";
    String reactionId = "like";

    when(redisOperations.set(userReactionKey, reactionId)).thenReturn(Mono.just(true));
    when(redisOperations.get(globalIncrementReactionKey)).thenReturn(Mono.just("5"));
    when(redisOperations.increment(globalIncrementReactionKey)).thenReturn(Mono.just(6L));

    Mono<Long> result =
        redisReactionRepository.saveReaction(
            userReactionKey, globalIncrementReactionKey, reactionId);

    StepVerifier.create(result).expectNext(6L).expectComplete().verify();

    verify(redisOperations).set(userReactionKey, reactionId);
    verify(redisOperations).get(globalIncrementReactionKey);
    // verify(redisOperations).increment(globalIncrementReactionKey);
  }

  @Test
  void testGetReactions() {
    List<String> keys = Arrays.asList("key1", "key2", "key3");

    when(redisOperations.multiGet(keys))
        .thenReturn(Mono.just(Arrays.asList("value1", "value2", "value3")));

    Mono<List<String>> result = redisReactionRepository.getReactions(keys);

    StepVerifier.create(result)
        .expectNext(Arrays.asList("value1", "value2", "value3"))
        .expectComplete()
        .verify();

    verify(redisOperations).multiGet(keys);
  }

  @Test
  void testUpdateReaction1() {
    String userReactionKey = "user_reaction_key";
    String incrementReactionKey = "increment_reaction_key";
    String newReaction = "new_reaction";
    UserReactionDTO userReactionDTO = new UserReactionDTO("1", "1", "1", Reaction.REACTION1);
    String oldReaction = "old_reaction";

    Mockito.when(redisOperations.getAndSet(userReactionKey, newReaction))
        .thenReturn(Mono.just(oldReaction));
    Mockito.when(redisOperations.decrement(any())).thenReturn(Mono.just(1L));
    Mockito.when(redisOperations.increment(incrementReactionKey)).thenReturn(Mono.just(2L));
    Mono<Long> result =
        redisReactionRepository.updateReaction(
            userReactionDTO, userReactionKey, incrementReactionKey, newReaction);

    // Assert
    assertEquals(2L, result.block());
  }

  @Test
  void testSaveMongoUserDataIntoRedis() {
    Map<String, String> userKeys = Collections.singletonMap("key1", "value1");

    when(redisOperations.multiSet(userKeys)).thenReturn(Mono.just(true));

    Mono<Boolean> result = redisReactionRepository.saveMongoUserDataIntoRedis(userKeys);

    StepVerifier.create(result).expectNext(true).expectComplete().verify();

    verify(redisOperations).multiSet(userKeys);
  }

  @Test
  void testSaveMongoGlobalCountDataIntoRedis() {
    Map<String, Long> globalCountKeys = Collections.singletonMap("key1", 42L);

    when(redisLongOperations.multiSet(globalCountKeys)).thenReturn(Mono.just(true));

    Mono<Boolean> result =
        redisReactionRepository.saveMongoGlobalCountDataIntoRedis(globalCountKeys);

    StepVerifier.create(result).expectNext(true).expectComplete().verify();

    verify(redisLongOperations).multiSet(globalCountKeys);
  }

  // Helper method to mimic your original method
  private String getGlobalIncrementOrDecrementReactionKey(
      UserReactionDTO dto, Optional<String> oldReaction) {
    return "global:increment:reaction";
  }

  @Test
  void testErrorDTOConstructor() {
    // Valid data
    ErrorCode errorCode = ErrorCode.NOT_FOUND;
    String errorMessage = "An internal error occurred.";
    OffsetDateTime timestamp = OffsetDateTime.now();
    ErrorDTO errorDTO = new ErrorDTO(errorCode, errorMessage, timestamp);
    assertNotNull(errorDTO);
    assertEquals(errorCode, errorDTO.errorCode());
    assertEquals(errorMessage, errorDTO.errorMessage());
    assertEquals(timestamp, errorDTO.timestamp());
    assertThrows(BadRequestException.class, () -> new ErrorDTO(null, errorMessage, timestamp));
    assertThrows(BadRequestException.class, () -> new ErrorDTO(errorCode, null, timestamp));
    assertThrows(BadRequestException.class, () -> new ErrorDTO(errorCode, errorMessage, null));
  }
}
