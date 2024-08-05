package com.ladbrokescoral.oxygen.service.betpack;

import com.ladbrokescoral.oxygen.dto.messages.BetPackMessage;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

@Component
public class BetPackRedisOperationsImpl implements BetPackRedisOperations {

  private final BetPackLastMessageCache betPackLastMessageCache;

  @Autowired
  public BetPackRedisOperationsImpl(
      @Qualifier("betPackLastMessageCache") BetPackLastMessageCache betPackLastMessageCache) {
    this.betPackLastMessageCache = betPackLastMessageCache;
  }

  @Override
  @Async
  public CompletableFuture<Optional<BetPackMessage>> getLastMessage(String channel) {
    Optional<BetPackMessage> message = betPackLastMessageCache.findById(channel);
    return CompletableFuture.completedFuture(message);
  }

  @Override
  @Async
  public void saveLastMessage(BetPackMessage message) {
    betPackLastMessageCache.save(message);
  }

  @Override
  public Optional<BetPackMessage> getLastSavedMessage(String channel) {
    return betPackLastMessageCache.findById(channel);
  }
}
