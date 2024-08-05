package com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;

import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetOffer;
import java.util.Arrays;
import java.util.List;
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

  @Mock private BetPackLastMessageCache betPackLastMessageCache;

  @InjectMocks private BetPackRedisOperationsImpl betPackRedisOperations;

  private BetPackMessage betPackMessage;

  @BeforeEach
  void setUp() {
    betPackMessage = new BetPackMessage("betPackId", new FreebetOffer());
    betPackRedisOperations = new BetPackRedisOperationsImpl(betPackLastMessageCache);
  }

  @Test
  void getLastMessageTest() {
    given(betPackLastMessageCache.findById(anyString())).willReturn(Optional.of(betPackMessage));
    CompletableFuture<Optional<BetPackMessage>> completableFuture =
        betPackRedisOperations.getLastMessage("");
    Assertions.assertNotNull(completableFuture);
  }

  @Test
  void saveLastMessageTest() {
    given(betPackLastMessageCache.save(any(BetPackMessage.class))).willReturn(betPackMessage);
    Assertions.assertDoesNotThrow(() -> betPackRedisOperations.saveLastMessage(betPackMessage));
  }

  @Test
  void getLastSavedMessageTest() {
    given(betPackLastMessageCache.findById(anyString())).willReturn(Optional.of(betPackMessage));
    Optional<BetPackMessage> betPackMessage = betPackRedisOperations.getLastSavedMessage("channel");
    Assertions.assertNotNull(betPackMessage);
  }

  @Test
  void getAllTest() {
    given(betPackLastMessageCache.findAll()).willReturn(Arrays.asList(betPackMessage));
    List<BetPackMessage> packMessageList = betPackRedisOperations.getAll();
    Assertions.assertNotNull(packMessageList);
  }
}
