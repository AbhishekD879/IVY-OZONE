package com.ladbrokescoral.oxygen.listeners;

import static org.mockito.Mockito.*;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class IncidentsUnsubscribeListenerTest {

  IncidentsUnsubscribeListener incidentsUnsubscribeListener;
  @Mock SocketIOClient socketClient;
  String eventId = "sFACTS222211218";

  @BeforeEach
  public void init() {
    incidentsUnsubscribeListener = new IncidentsUnsubscribeListener();
  }

  @Test
  void onDataTest() throws Exception {
    AckRequest ackSender = null;
    incidentsUnsubscribeListener.onData(socketClient, eventId, ackSender);
    verify(socketClient, timeout(500)).disconnect();
  }

  @Test
  void onDataChannelOpenTest() throws Exception {
    AckRequest ackSender = null;
    when(socketClient.isChannelOpen()).thenReturn(true);
    incidentsUnsubscribeListener.onData(socketClient, eventId, ackSender);
    verify(socketClient, timeout(500)).leaveRoom(eventId.substring(6));
  }
}
