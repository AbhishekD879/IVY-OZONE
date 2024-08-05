package com.ladbrokescoral.reactions.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.reactions.dto.AggregateKeys;
import com.ladbrokescoral.reactions.dto.GlobalCount;
import com.ladbrokescoral.reactions.repository.mongo.MongoUserRepository;
import com.ladbrokescoral.reactions.repository.mongo.MongoUserSortingRepository;
import com.ladbrokescoral.reactions.repository.mongo.entity.MongoUserEntity;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.data.domain.Pageable;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

class DefaultMongoReactionServiceTest {

  @InjectMocks private DefaultMongoReactionService mongoReactionService;

  @Mock private MongoUserRepository userRepository;

  @Mock private MongoUserSortingRepository sortingRepository;

  @BeforeEach
  public void setUp() {
    MockitoAnnotations.initMocks(this);
  }

  @Test
  void testSaveUser() {
    MongoUserEntity userEntity = new MongoUserEntity("1", "2", "3");
    when(userRepository.save(userEntity)).thenReturn(Mono.just(userEntity));

    Mono<MongoUserEntity> savedUser = mongoReactionService.saveUser(userEntity);

    assertEquals(userEntity, savedUser.block());
  }

  @Test
  void testUpdateUser() {
    String userId = "1";
    MongoUserEntity userEntity = new MongoUserEntity("1", "2", "3");
    when(userRepository.findById(userId)).thenReturn(Mono.just(userEntity));
    when(userRepository.save(userEntity)).thenReturn(Mono.just(userEntity));

    Mono<MongoUserEntity> updatedUser = mongoReactionService.updateUser(userEntity);

    assertEquals(userEntity, updatedUser.block());
  }

  @Test
  void testGetAllUserDeleteKeys() {
    List<String> deleteKeys = List.of("3");
    MongoUserEntity userEntity = new MongoUserEntity("1", "2", "3");
    when(userRepository.findAll())
        .thenReturn(Flux.just(userEntity)); // Mock an empty user list for simplicity

    Flux<String> userDeleteKeys = mongoReactionService.getAllUserDeleteKeys();

    assertEquals(deleteKeys, userDeleteKeys.collectList().block());
  }

  // Similar tests can be written for other methods following the same pattern

  @Test
  void testDeleteUsers() {
    List<String> deleteKeys = List.of("key1", "key2");
    when(userRepository.deleteAllByDeleteKeys(deleteKeys)).thenReturn(Mono.empty());

    Mono<Void> result = mongoReactionService.deleteUsers(deleteKeys);

    verify(userRepository, times(1)).deleteAllByDeleteKeys(deleteKeys);
  }

  @Test
  void testGetReactionGlobalCount() {
    String deleteKey = "key";
    String reactionType = "like";
    long count = 42L;

    when(userRepository.getReactionGlobalCount())
        .thenReturn(Flux.just(new GlobalCount(new AggregateKeys("deleteKey", "deleteKey"), count)));
    mongoReactionService.getReactionGlobalCount();

    verify(userRepository, times(1)).getReactionGlobalCount();
  }

  @Test
  void testGetUsersCount() {
    long count = 100L;

    when(userRepository.getUsersCount()).thenReturn(Mono.just(count));

    StepVerifier.create(mongoReactionService.getUsersCount())
        .expectNext(count)
        .expectComplete()
        .verify();

    verify(userRepository, times(1)).getUsersCount();
  }

  @Test
  void testFindAllPaginatedUsers() {
    Pageable pageable = Pageable.ofSize(10).withPage(1);

    Map<String, String> userMap = new HashMap<>();
    userMap.put("key1", "value1");
    MongoUserEntity userEntity = new MongoUserEntity("key1", "value1", "3");
    when(sortingRepository.findAllBy(pageable)).thenReturn(Flux.just(userEntity));

    StepVerifier.create(mongoReactionService.findAllPaginatedUsers(pageable))
        .expectNext(userMap)
        .expectComplete()
        .verify();

    verify(sortingRepository, times(1)).findAllBy(pageable);
  }
}
