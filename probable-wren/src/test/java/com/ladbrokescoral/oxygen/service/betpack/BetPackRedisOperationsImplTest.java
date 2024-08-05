package com.ladbrokescoral.oxygen.service.betpack;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;

import com.ladbrokescoral.oxygen.dto.messages.BetPackMessage;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class BetPackRedisOperationsImplTest implements WithAssertions {

  private final String CHANNEL = "redis_operations _channel";

  @Mock private BetPackLastMessageCache betPackLastMessageCache;

  @InjectMocks private BetPackRedisOperationsImpl betPackRedisOperations;

  @BeforeEach
  public void init() {
    betPackRedisOperations = new BetPackRedisOperationsImpl(betPackLastMessageCache);
  }

  @Test
  void getLastMessage() {
    given(betPackLastMessageCache.findById(CHANNEL)).willReturn(Optional.of(new BetPackMessage()));
    CompletableFuture<Optional<BetPackMessage>> expected =
        betPackRedisOperations.getLastMessage(CHANNEL);
    assertNotNull(expected);
    Assertions.assertDoesNotThrow(() -> betPackRedisOperations.getLastMessage(CHANNEL));
  }

  @Test
  void saveLastMessageTest() {
    BetPackMessage entity = new BetPackMessage();
    entity.setBetPackId("1");
    given(betPackLastMessageCache.save(any(BetPackMessage.class))).willReturn(entity);
    betPackRedisOperations.saveLastMessage(entity);
    assertNotNull(entity);
  }

  @Test
  void getLastSavedMessage() {
    given(betPackLastMessageCache.findById(CHANNEL)).willReturn(Optional.of(new BetPackMessage()));
    Optional<BetPackMessage> expected = betPackRedisOperations.getLastSavedMessage(CHANNEL);
    assertNotNull(expected);
    Assertions.assertDoesNotThrow(() -> betPackRedisOperations.getLastSavedMessage(CHANNEL));
  }
}
