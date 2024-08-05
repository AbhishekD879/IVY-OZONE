package com.coral.oxygen.middleware.ms.quickbet.impl;

import static org.assertj.core.api.Java6Assertions.assertThatCode;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.time.Duration;
import org.assertj.core.api.Fail;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.redisson.Redisson;
import org.redisson.api.RLock;

class RedissonLockOnceExecutorTest {

  private Redisson redissonMock;
  private OnceExecutor onceExecutor;
  private RLock rlockMock;

  @BeforeEach
  void setUp() {
    redissonMock = Mockito.mock(Redisson.class);
    rlockMock = Mockito.mock(RLock.class);
    when(redissonMock.getFairLock(any())).thenReturn(rlockMock);

    onceExecutor = new RedissonLockOnceExecutor(redissonMock);
  }

  @Test
  void ifNotLockedThenActionIsExecuted() {
    when(rlockMock.isLocked()).thenReturn(false);
    when(rlockMock.isHeldByCurrentThread()).thenReturn(true);

    onceExecutor.executeOnceDuringTimePeriod(
        "123", () -> {}, () -> Fail.fail("Action shouldn't execute"), Duration.ofSeconds(1));

    verify(rlockMock).unlock();
  }

  @Test
  void ifLockedThenRejectActionIsExecuted() {
    when(rlockMock.isLocked()).thenReturn(true);
    assertThatCode(
            () ->
                onceExecutor.executeOnceDuringTimePeriod(
                    "123",
                    () -> Fail.fail("Action shouldn't execute"),
                    () -> {},
                    Duration.ofSeconds(1)))
        .doesNotThrowAnyException();
  }
}
