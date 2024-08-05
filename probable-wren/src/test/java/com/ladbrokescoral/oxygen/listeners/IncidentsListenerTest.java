package com.ladbrokescoral.oxygen.listeners;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.*;
import static org.mockito.Mockito.when;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.HandshakeData;
import com.corundumstudio.socketio.SocketIOClient;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class IncidentsListenerTest {

  IncidentsListener incidentsListener;
  @Mock SocketIOClient client;
  String eventId = "sFACTS222211218";

  @BeforeEach
  public void init() {
    incidentsListener = new IncidentsListener();
  }

  @Test
  void onDataTest() throws Exception {
    when(client.getHandshakeData()).thenReturn(new HandshakeData());
    incidentsListener.onData(client, eventId, null);
    verify(client, times(0)).sendEvent(any(), any());
  }

  @Test
  void onDataTestIsChannelOpenTestFalse() throws Exception {
    AckRequest ackSender = null;
    when(client.isChannelOpen()).thenReturn(false);
    when(client.getHandshakeData()).thenReturn(new HandshakeData());
    incidentsListener.onData(client, eventId, ackSender);
    assertNotNull(eventId);
  }

  @Test
  void onDataTestIsChannelOpenTestTrue() throws Exception {
    AckRequest ackSender = null;
    when(client.isChannelOpen()).thenReturn(true);
    incidentsListener.onData(client, eventId, ackSender);
    assertNotNull(eventId);
  }
}
