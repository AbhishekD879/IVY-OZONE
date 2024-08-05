package com.ladbrokescoral.oxygen.service;

import static org.mockito.Mockito.*;

import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.listener.DataListener;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.ladbrokescoral.oxygen.listeners.IncidentsListener;
import com.ladbrokescoral.oxygen.listeners.MatchFactCodesListener;
import com.ladbrokescoral.oxygen.listeners.ThrottleLogic;
import com.ladbrokescoral.oxygen.service.betpack.BetPackRedisOperations;
import com.ladbrokescoral.oxygen.utils.EnvironmentProvider;
import java.util.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class SocketIOListenerTest {

  @Mock private SocketIOServer socketIOServer;
  @Mock private EnvironmentProvider environmentProvider;
  @Mock private KafkaPublisherImpl kafkaPublisherImpl;
  @Mock private RedisOperations redisOperations;
  @Mock private SocketIOClient socketIOClient;
  @Mock private ThrottleLogic throttleLogic;
  private Gson gson;
  private SocketIOListener socketIOListener;
  @Mock private LeaderboardSocketIOHelper leaderboardSocketIOHelper;
  @Mock private DataListener<String> scoreboardListener;
  @Mock private IncidentsListener incidentsListener;
  @Mock private MatchFactCodesListener matchFactCodesListener;
  @Mock private LeaderboardSubscriptionHelper leaderboardSubscriptionHelper;
  @Mock private BetPackKafkaPublisher betPackKafkaPublisher;
  @Mock private BetPackRedisOperations betPackRedisOperations;

  @BeforeEach
  public void init() {
    gson = new GsonBuilder().serializeNulls().create();
    socketIOListener =
        new SocketIOListener(
            socketIOServer,
            environmentProvider,
            gson,
            kafkaPublisherImpl,
            redisOperations,
            Optional.of(leaderboardSocketIOHelper),
            throttleLogic,
            scoreboardListener,
            incidentsListener,
            Optional.of(leaderboardSubscriptionHelper),
            betPackKafkaPublisher,
            betPackRedisOperations,
            matchFactCodesListener);

    when(socketIOClient.getSessionId()).thenReturn(UUID.randomUUID());
  }

  @Test
  void socketIOServerStartTest() {
    socketIOListener.start();
    verify(socketIOServer, times(1)).start();
    socketIOListener.onConnect(socketIOClient);
  }

  @Test
  void socketIOServerStopTest() {
    Set<String> set = new HashSet<>(Arrays.asList("c::1", "c::2", "c::3"));
    when(socketIOClient.getAllRooms()).thenReturn(set);
    when(socketIOServer.getAllClients()).thenReturn(Collections.singleton(socketIOClient));
    socketIOListener.stop();
    socketIOListener.onDisconnect(socketIOClient);
    verify(socketIOServer, times(1)).stop();
  }

  @Test
  void socketIOServerStopTest1() {
    Set<String> set = new HashSet<>();
    when(socketIOClient.getAllRooms()).thenReturn(set);
    when(socketIOServer.getAllClients()).thenReturn(Collections.singleton(socketIOClient));
    socketIOListener.stop();
    socketIOListener.onDisconnect(socketIOClient);
    verify(socketIOServer, times(1)).stop();
  }
}
