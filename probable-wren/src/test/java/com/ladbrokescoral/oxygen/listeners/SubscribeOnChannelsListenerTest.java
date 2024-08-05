package com.ladbrokescoral.oxygen.listeners;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.corundumstudio.socketio.HandshakeData;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.ladbrokescoral.oxygen.dto.messages.SimpleMessage;
import com.ladbrokescoral.oxygen.dto.messages.SubscriptionAck;
import com.ladbrokescoral.oxygen.service.KafkaPublisherImpl;
import com.ladbrokescoral.oxygen.service.RedisOperations;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
public class SubscribeOnChannelsListenerTest {

  @Mock private SocketIOServer socketIOServer;
  @Mock private KafkaPublisherImpl kafkaPublisherImpl;
  @Mock private RedisOperations redisOperations;
  @Mock private CompletableFuture<Optional<SimpleMessage>> redisResponse;
  @Mock SocketIOClient socketClient;
  @Mock ThrottleLogic throttleLogic;

  private SubscribeOnChannelsListener listener;

  private static final String CHANNEL = "sEVMKT0150171598";
  private static final String MESSAGE =
      "{'type':'SUBSCRIBED','message':{'channel':'sEVMKT0150171598'}}";

  @BeforeEach
  public void init() {
    Gson gson = new GsonBuilder().serializeNulls().create();
    listener =
        new SubscribeOnChannelsListener(
            socketIOServer, kafkaPublisherImpl, redisOperations, gson, throttleLogic);
  }

  @Test
  public void onDataTestSocketNotOpen() {
    when(socketClient.getHandshakeData()).thenReturn(new HandshakeData());

    List<String> channelsList = Arrays.asList(CHANNEL);
    listener.onData(socketClient, channelsList, null);
  }

  @Test
  public void onDataTest() {
    when(redisOperations.getLastMessage(CHANNEL))
        .thenReturn(
            CompletableFuture.completedFuture(Optional.of(new SimpleMessage(CHANNEL, MESSAGE))));
    when(socketClient.getAllRooms()).thenReturn(Collections.singleton(CHANNEL));
    when(socketClient.isChannelOpen()).thenReturn(true);
    List<String> channelsList = Arrays.asList(CHANNEL);
    listener.onData(socketClient, channelsList, null);
    verify(kafkaPublisherImpl).publish(CHANNEL, null);
    verify(socketClient).sendEvent(eq(CHANNEL), any(SubscriptionAck.class));
  }

  @Test
  public void onDataTestWithoutLastMessage() {
    when(redisOperations.getLastMessage(CHANNEL))
        .thenReturn(CompletableFuture.completedFuture(Optional.empty()));
    List<String> channelsList =
        Arrays.asList(
            CHANNEL,
            "SEVENT0010049893",
            "EVENT00010049893",
            "SCORE00010049893",
            "CLOCK00010049893");
    when(socketClient.isChannelOpen()).thenReturn(true);
    listener.onData(socketClient, channelsList, null);
    verify(kafkaPublisherImpl).publish(CHANNEL, null);
    verify(socketClient, times(0)).sendEvent(any(), any());
  }

  @Test
  void onDataHackerDetectedTest() {
    when(throttleLogic.hackerDetected(any(), any())).thenReturn(true);

    List<String> channelsList = Arrays.asList(CHANNEL, "SEVENT0010049893");
    listener.onData(socketClient, channelsList, null);

    verify(kafkaPublisherImpl, times(0)).publish(CHANNEL, null);
  }
}
