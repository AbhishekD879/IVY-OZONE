package com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

/*
 This class is processing bet pack updates.
*/
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
  public CompletableFuture<Optional<BetPackMessage>> getLastMessage(String betPackId) {
    Optional<BetPackMessage> message = betPackLastMessageCache.findById(betPackId);
    return CompletableFuture.completedFuture(message);
  }

  @Override
  @Async
  public void saveLastMessage(BetPackMessage message) {
    betPackLastMessageCache.save(message);
  }

  @Override
  public Optional<BetPackMessage> getLastSavedMessage(String betPackId) {
    return betPackLastMessageCache.findById(betPackId);
  }

  public List<BetPackMessage> getAll() {
    return (List<BetPackMessage>) betPackLastMessageCache.findAll();
  }
}
