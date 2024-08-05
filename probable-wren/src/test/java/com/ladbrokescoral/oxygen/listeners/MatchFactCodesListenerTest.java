package com.ladbrokescoral.oxygen.listeners;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import com.corundumstudio.socketio.SocketIOClient;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.dto.messages.IncidentMessage;
import com.ladbrokescoral.oxygen.service.RedisOperations;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class MatchFactCodesListenerTest {

  MatchFactCodesListener matchFactCodesListener;
  @Mock RedisOperations redisOperations;
  @Mock SocketIOClient client;
  List<String> data = Arrays.asList("mFACTS12286416");
  String CHANNEL = "12286416";
  long ttl = 0;
  String MESSAGE =
      "{\"incident\":{\"eventId\":\"fake593f-d146-4092-ad46-8bdf192b6ebb\",\"correlationId\":\"7645316d-ddc8-42c9-ac4e-e6668704a5f6\",\"seqId\":null,\"type\":{\"code\":601,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2022-01-03T12:43:40.342Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";

  @BeforeEach
  void init() {
    matchFactCodesListener = new MatchFactCodesListener(redisOperations, new ObjectMapper());
  }

  @Test
  void onDataMatchFactCodeTest() throws Exception {
    when(redisOperations.getIncidentLastMessage(CHANNEL))
        .thenReturn(
            CompletableFuture.completedFuture(
                Optional.of(new IncidentMessage(CHANNEL, MESSAGE, ttl))));
    redisOperations.saveLastIncidentMessage(new IncidentMessage(CHANNEL, MESSAGE, ttl));
    matchFactCodesListener.onData(client, data, null);
    String strVal = "mFACTS" + CHANNEL;
    verify(client).sendEvent(eq(strVal), any());
  }

  @Test
  void onDataEmptyMatchFactCodeTest() throws Exception {
    when(redisOperations.getIncidentLastMessage(CHANNEL))
        .thenReturn(CompletableFuture.completedFuture(Optional.empty()));
    redisOperations.saveLastIncidentMessage(new IncidentMessage(CHANNEL, MESSAGE, ttl));
    matchFactCodesListener.onData(client, data, null);
    String strVal = "mFACTS" + CHANNEL;
    verify(client, times(0)).sendEvent(any(), any());
  }

  @Test
  void onDataExceptionTest() throws Exception {
    String MESSAGE = "{'type':'SUBSCRIBED','message':{'channel':'sEVMKT0150171598'}}";
    when(redisOperations.getIncidentLastMessage(CHANNEL))
        .thenReturn(
            CompletableFuture.completedFuture(
                Optional.of(new IncidentMessage(CHANNEL, MESSAGE, ttl))));
    matchFactCodesListener.onData(client, data, null);
    verify(client, times(0)).sendEvent(any(), any());
  }
}
