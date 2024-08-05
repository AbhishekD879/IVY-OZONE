package com.ladbrokescoral.oxygen.service;

import com.ladbrokescoral.oxygen.dto.messages.IncidentMessage;
import com.ladbrokescoral.oxygen.dto.messages.SimpleMessage;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

@Component
public class RedisOperationsImpl implements RedisOperations {

  private final LastMessageCache lastMessageCache;
  private final LastIncidentCache lastIncidentCache;

  @Autowired
  public RedisOperationsImpl(
      @Qualifier("lastMessageCache") LastMessageCache lastMessageCache,
      LastIncidentCache lastIncidentCache) {
    this.lastMessageCache = lastMessageCache;
    this.lastIncidentCache = lastIncidentCache;
  }

  @Override
  @Async
  public CompletableFuture<Optional<SimpleMessage>> getLastMessage(String channel) {
    Optional<SimpleMessage> message = lastMessageCache.findById(channel);
    return CompletableFuture.completedFuture(message);
  }

  @Override
  @Async
  public void saveLastMessage(SimpleMessage message) {
    lastMessageCache.save(message);
  }

  @Override
  public CompletableFuture<Optional<IncidentMessage>> getIncidentLastMessage(String channel) {
    Optional<IncidentMessage> message = lastIncidentCache.findById(channel);
    return CompletableFuture.completedFuture(message);
  }

  @Override
  public void saveLastIncidentMessage(IncidentMessage message) {
    lastIncidentCache.save(message);
  }

  @Override
  public void clearIncidentMessage(IncidentMessage message) {
    lastIncidentCache.delete(message);
  }
}
