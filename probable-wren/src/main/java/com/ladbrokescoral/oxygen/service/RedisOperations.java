package com.ladbrokescoral.oxygen.service;

import com.ladbrokescoral.oxygen.dto.messages.IncidentMessage;
import com.ladbrokescoral.oxygen.dto.messages.SimpleMessage;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;

public interface RedisOperations {

  CompletableFuture<Optional<SimpleMessage>> getLastMessage(String channel);

  void saveLastMessage(SimpleMessage message);

  CompletableFuture<Optional<IncidentMessage>> getIncidentLastMessage(String channel);

  void saveLastIncidentMessage(IncidentMessage message);

  void clearIncidentMessage(IncidentMessage message);
}
