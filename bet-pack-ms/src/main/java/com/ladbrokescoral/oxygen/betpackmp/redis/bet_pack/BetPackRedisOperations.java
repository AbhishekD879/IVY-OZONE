package com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack;

import java.util.Optional;
import java.util.concurrent.CompletableFuture;

public interface BetPackRedisOperations {

  CompletableFuture<Optional<BetPackMessage>> getLastMessage(String channel);

  void saveLastMessage(BetPackMessage message);

  Optional<BetPackMessage> getLastSavedMessage(String channel);
}
