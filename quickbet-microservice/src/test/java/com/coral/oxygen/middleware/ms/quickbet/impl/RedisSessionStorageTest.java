package com.coral.oxygen.middleware.ms.quickbet.impl;

import static org.mockito.Mockito.mock;
import static reactor.core.publisher.Mono.when;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import java.util.Collections;
import java.util.List;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.redis.core.BoundValueOperations;
import org.springframework.data.redis.core.RedisTemplate;

@ExtendWith(MockitoExtension.class)
class RedisSessionStorageTest {
  RedisTemplate redisTemplateMock = mock(RedisTemplate.class);
  BoundValueOperations valueOperations = mock(BoundValueOperations.class);
  RedisSessionStorage redisSessionStorage = new RedisSessionStorage(redisTemplateMock, 2l);

  @Test
  void testRefreshTtlFalse() {
    Mockito.doReturn(valueOperations).when(redisTemplateMock).boundValueOps(Mockito.any());
    Mockito.when(
            redisTemplateMock.boundValueOps(Mockito.any()).expire(Mockito.anyLong(), Mockito.any()))
        .thenReturn(false);
    Assertions.assertFalse(redisSessionStorage.refreshTtl("222222"));
  }

  @Test
  void testRefreshTtlNull() {
    Mockito.doReturn(valueOperations).when(redisTemplateMock).boundValueOps(Mockito.any());
    Mockito.when(
            redisTemplateMock.boundValueOps(Mockito.any()).expire(Mockito.anyLong(), Mockito.any()))
        .thenReturn(null);
    Assertions.assertFalse(redisSessionStorage.refreshTtl("222222"));
  }

  @Test
  void testPersist() {
    try {
      SessionDto sessionDto = new SessionDto("123");
      Mockito.when(redisTemplateMock.boundValueOps(sessionDto.getSessionId()))
          .thenReturn(valueOperations);
      redisSessionStorage.persist(sessionDto);
    } catch (Exception e) {
      Assertions.assertNotNull(e);
    }
  }

  @Test
  void findTest() {
    SessionDto sessionDto = new SessionDto("7687");
    Mockito.when(redisTemplateMock.boundValueOps(sessionDto.getSessionId()))
        .thenReturn(valueOperations);
    Mockito.when(valueOperations.get()).thenReturn(sessionDto);
    Assertions.assertNotNull(redisSessionStorage.find(sessionDto.getSessionId()));
  }

  @Test
  void testRedisKeys() {
    Mockito.doReturn(Collections.singleton("key1")).when(redisTemplateMock).keys(Mockito.any());
    Mockito.doReturn(valueOperations).when(redisTemplateMock).boundValueOps(Mockito.any());
    List<SessionDto> all = redisSessionStorage.findAll();
    Assertions.assertFalse(all.isEmpty());
  }

  @Test
  void testRedisEmptyKeys() {
    when(redisTemplateMock.keys("*")).thenReturn(Collections.emptyList());
    List<SessionDto> all = redisSessionStorage.findAll();
    Assertions.assertTrue(all.isEmpty());
  }
}
