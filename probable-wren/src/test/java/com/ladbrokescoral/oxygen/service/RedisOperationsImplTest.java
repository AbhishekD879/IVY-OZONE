package com.ladbrokescoral.oxygen.service;

import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.dto.messages.IncidentMessage;
import com.ladbrokescoral.oxygen.dto.messages.SimpleMessage;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class RedisOperationsImplTest {

  @Mock LastIncidentCache lastIncidentCache;
  @Mock LastMessageCache lastMessageCache;
  RedisOperationsImpl redisOperations;
  String CHANNEL = "222211218";
  private static final String MESSAGE =
      "{'type':'SUBSCRIBED','message':{'channel':'sEVMKT0150171598'}}";
  long ttl = 900;
  String INC_MESSAGE =
      "{\"incident\":{\"eventId\":\"fake593f-d146-4092-ad46-8bdf192b6ebb\",\"correlationId\":\"7645316d-ddc8-42c9-ac4e-e6668704a5f6\",\"seqId\":null,\"type\":{\"code\":601,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2022-01-03T12:43:40.342Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";

  @BeforeEach
  public void init() {
    redisOperations = new RedisOperationsImpl(lastMessageCache, lastIncidentCache);
  }

  @Test
  void getLastMessageTest() {
    when(lastMessageCache.findById(CHANNEL))
        .thenReturn(Optional.of(new SimpleMessage(CHANNEL, MESSAGE)));
    CompletableFuture<Optional<SimpleMessage>> simCompletableFuture =
        redisOperations.getLastMessage(CHANNEL);
    Assertions.assertNotNull(simCompletableFuture);
  }

  @Test
  void getLastIncidentMessageTest() {
    when(lastIncidentCache.findById(CHANNEL))
        .thenReturn(Optional.of(new IncidentMessage(CHANNEL, INC_MESSAGE, ttl)));
    CompletableFuture<Optional<IncidentMessage>> optionalIncidentMessage =
        redisOperations.getIncidentLastMessage(CHANNEL);
    Assertions.assertNotNull(optionalIncidentMessage);
  }

  @Test
  void saveLastIncidentMessage() {
    redisOperations.saveLastIncidentMessage(new IncidentMessage(CHANNEL, INC_MESSAGE, ttl));
    verify(lastIncidentCache, times(1)).save(any());
  }

  @Test
  void saveLastMessage() {
    redisOperations.saveLastMessage(new SimpleMessage(CHANNEL, MESSAGE));
    verify(lastMessageCache, times(1)).save(any());
  }

  @Test
  void clearIncidentMessage() {
    redisOperations.clearIncidentMessage(new IncidentMessage());
    verify(lastIncidentCache, times(1)).delete(new IncidentMessage());
  }
}
