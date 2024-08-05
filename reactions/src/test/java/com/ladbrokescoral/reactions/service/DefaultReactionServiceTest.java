package com.ladbrokescoral.reactions.service;

import static org.mockito.Mockito.*;

import com.ladbrokescoral.reactions.client.bpp.BppClient;
import com.ladbrokescoral.reactions.client.bpp.dto.UserData;
import com.ladbrokescoral.reactions.dto.*;
import com.ladbrokescoral.reactions.exception.ServiceExecutionException;
import com.ladbrokescoral.reactions.repository.mongo.entity.MongoUserEntity;
import com.ladbrokescoral.reactions.repository.redis.RedisReactionRepository;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

class DefaultReactionServiceTest {

  @InjectMocks private DefaultReactionService reactionService;

  @Mock private RedisReactionRepository redisRepository;

  @Mock private MongoReactionService mongoReactionService;
  @Mock private BppClient bppClient;

  @BeforeEach
  public void setUp() {
    MockitoAnnotations.initMocks(this);
  }

  @Test
  void testSaveReaction() {
    String token = "user123";
    String userName = "user123";
    UserData userData = new UserData("user123", "user123", true);
    MongoUserEntity userEntity = new MongoUserEntity("1", "2", "3");
    UserReactionDTO userReactionDTO = new UserReactionDTO("1", "1", "1", Reaction.REACTION1);
    when(redisRepository.saveReaction(anyString(), anyString(), anyString()))
        .thenReturn(Mono.just(1l));
    when(mongoReactionService.saveUser(any())).thenReturn(Mono.just(userEntity));
    when(bppClient.getValidUser(any())).thenReturn(Mono.just(userData));
    StepVerifier.create(reactionService.saveReaction(token, userName, userReactionDTO))
        .expectNext(true)
        .expectComplete()
        .verify();
    verify(redisRepository, times(1)).saveReaction(anyString(), anyString(), anyString());
    verify(mongoReactionService, times(1)).saveUser(any());
  }

  @Test
  void testSaveReactionError() {
    String token = "user123";
    String userName = "test";
    UserData userData = new UserData("user123", "user123", true);
    MongoUserEntity userEntity = new MongoUserEntity("1", "2", "3");
    UserReactionDTO userReactionDTO = new UserReactionDTO("1", "1", "1", Reaction.REACTION1);
    when(redisRepository.saveReaction(anyString(), anyString(), anyString()))
        .thenReturn(Mono.just(1l));
    when(mongoReactionService.saveUser(any())).thenReturn(Mono.just(userEntity));
    when(bppClient.getValidUser(any())).thenReturn(Mono.just(userData));
    StepVerifier.create(reactionService.saveReaction(token, userName, userReactionDTO))
        .expectError()
        .verify();
  }

  @Test
  void testSaveReaction1() {
    String token = "user123";
    String userName = "user123";
    UserData userData = new UserData("user123", "user123", true);
    MongoUserEntity userEntity = new MongoUserEntity("1", "2", "3");
    UserReactionDTO userReactionDTO = new UserReactionDTO("1", "1", "1", Reaction.REACTION1);
    when(redisRepository.saveReaction(anyString(), anyString(), anyString()))
        .thenReturn(Mono.error(Throwable::new));
    when(mongoReactionService.saveUser(any())).thenReturn(Mono.just(userEntity));
    when(bppClient.getValidUser(any())).thenReturn(Mono.just(userData));
    StepVerifier.create(reactionService.saveReaction(token, userName, userReactionDTO))
        .expectError()
        .verify();
  }

  @Test
  void testUpdateReaction() {
    String token = "user123";
    String userName = "user123";
    UserData userData = new UserData("user123", "user123", true);
    MongoUserEntity userEntity = new MongoUserEntity("1", "2", "3");
    UserReactionDTO userReactionDTO = new UserReactionDTO("1", "1", "1", Reaction.REACTION1);
    when(redisRepository.updateReaction(any(), anyString(), anyString(), anyString()))
        .thenReturn(Mono.just(1l));
    when(mongoReactionService.updateUser(any())).thenReturn(Mono.just(userEntity));
    when(bppClient.getValidUser(any())).thenReturn(Mono.just(userData));
    StepVerifier.create(reactionService.updateReaction(token, userName, userReactionDTO))
        .expectNext("REACTION1")
        .expectComplete()
        .verify();
    verify(redisRepository, times(1)).updateReaction(any(), anyString(), anyString(), anyString());
    verify(mongoReactionService, times(1)).updateUser(any());
  }

  @Test
  void testUpdateReaction1() {
    String token = "user123";
    String userName = "user123";
    UserData userData = new UserData("user123", "user123", true);
    MongoUserEntity userEntity = new MongoUserEntity("1", "2", "3");
    UserReactionDTO userReactionDTO = new UserReactionDTO("1", "1", "1", Reaction.REACTION1);
    when(redisRepository.updateReaction(any(), anyString(), anyString(), anyString()))
        .thenReturn(Mono.error(Throwable::new));
    when(mongoReactionService.updateUser(any())).thenReturn(Mono.just(userEntity));
    when(bppClient.getValidUser(any())).thenReturn(Mono.just(userData));
    StepVerifier.create(reactionService.updateReaction(token, userName, userReactionDTO))
        .expectError()
        .verify();
  }

  @Test
  void testGetGlobalCount() {
    String custId = "customer123";
    SurfaceBetInfoRequestDTO surfaceBetInfoRequestDTO = new SurfaceBetInfoRequestDTO("1", "1");
    List<SurfaceBetInfoRequestDTO> requestDTO = List.of(surfaceBetInfoRequestDTO);
    when(redisRepository.getReactions(anyList()))
        .thenReturn(Mono.just(List.of("1", "1", "1", "1")));

    StepVerifier.create(reactionService.getGlobalCount(custId, requestDTO))
        .expectNextMatches(responseDTO -> responseDTO.custId().equalsIgnoreCase("customer123"))
        .expectComplete()
        .verify();
  }

  @Test
  void testGetGlobalCountException() {
    String custId = "customer123";
    SurfaceBetInfoRequestDTO surfaceBetInfoRequestDTO = new SurfaceBetInfoRequestDTO("1", "1");
    List<SurfaceBetInfoRequestDTO> requestDTO = List.of(surfaceBetInfoRequestDTO);
    when(redisRepository.getReactions(anyList()))
        .thenReturn(Mono.just(List.of("a", "a", "a", "a")));

    StepVerifier.create(reactionService.getGlobalCount(custId, requestDTO))
        .expectError(ServiceExecutionException.class)
        .verify();
  }

  @Test
  void testGetGlobalCount_onError() {
    String custId = "customer123";
    SurfaceBetInfoRequestDTO surfaceBetInfoRequestDTO = new SurfaceBetInfoRequestDTO("1", "1");
    List<SurfaceBetInfoRequestDTO> requestDTO = List.of(surfaceBetInfoRequestDTO);
    when(redisRepository.getReactions(anyList()))
        .thenReturn(Mono.error(new ServiceExecutionException("Invalid")));

    StepVerifier.create(reactionService.getGlobalCount(custId, requestDTO))
        .expectError(ServiceExecutionException.class)
        .verify();
  }

  @Test
  void testCollectGlobalCountFromMongo() {
    AggregateKeys aggregateKeys = new AggregateKeys("test", "test");
    GlobalCount globalCount = new GlobalCount(aggregateKeys, 10L);
    when(mongoReactionService.getAllUserDeleteKeys())
        .thenReturn(Flux.fromIterable(List.of("1", "1", "1", "1")));
    when(mongoReactionService.getReactionGlobalCount()).thenReturn(Flux.just(globalCount));
    Map<String, Long> rmap = new HashMap<>();
    rmap.put("test#test", 10l);
    StepVerifier.create(reactionService.collectGlobalCountFromMongo())
        .expectNext(rmap)
        .expectComplete()
        .verify();
    verify(mongoReactionService, atLeastOnce()).getReactionGlobalCount();
  }

  @Test
  void testGetUserReactedReaction()
      throws NoSuchMethodException, IllegalAccessException, InvocationTargetException {
    Class<DefaultReactionService> clazz = DefaultReactionService.class;
    Method met = clazz.getDeclaredMethod("getUserReactedReaction", List.class);
    met.setAccessible(true);
    try {
      String res =
          (String) met.invoke(reactionService, List.of("Reaction1", "Reaction2", "Reaction3", ""));
      String res1 =
          (String) met.invoke(reactionService, List.of("Reaction1", "Reaction2", "Reaction3", " "));
      String res2 =
          (String)
              met.invoke(reactionService, List.of("Reaction1", "Reaction2", "Reaction3", "test"));
      Assertions.assertNotNull(res2);
    } catch (Exception e) {
    }
  }

  @Test
  void testGetReactionCount()
      throws NoSuchMethodException, IllegalAccessException, InvocationTargetException {
    Class<DefaultReactionService> clazz = DefaultReactionService.class;
    Method met = clazz.getDeclaredMethod("getReactionCount", List.class, int.class);
    met.setAccessible(true);
    try {
      String res =
          (String)
              met.invoke(reactionService, List.of("Reaction1", "Reaction2", "Reaction3", ""), 3);
      String res1 =
          (String)
              met.invoke(reactionService, List.of("Reaction1", "Reaction2", "Reaction3", " "), 3);
      String res2 =
          (String)
              met.invoke(
                  reactionService, List.of("Reaction1", "Reaction2", "Reaction3", "test"), 3);
      Assertions.assertNotNull(res);
    } catch (Exception e) {
    }
  }
}
