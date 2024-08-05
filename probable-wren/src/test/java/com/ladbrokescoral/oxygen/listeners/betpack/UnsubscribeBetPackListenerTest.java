package com.ladbrokescoral.oxygen.listeners.betpack;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import static org.mockito.Mockito.when;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.HandshakeData;
import com.corundumstudio.socketio.SocketIOClient;
import java.util.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class UnsubscribeBetPackListenerTest {

  UnsubscribeBetPackListener unsubscribeBetPackListener;
  @Mock SocketIOClient socketClient;
  @Mock HandshakeData handshakeData;
  private static final String CHANNEL = "sEVMKT0150171598";

  @BeforeEach
  public void init() {
    unsubscribeBetPackListener = new UnsubscribeBetPackListener();
  }

  @Test
  void onDataTrue() throws Exception {
    String data = "222211218";
    AckRequest ackSender = null;
    Set<String> set = new HashSet<String>();
    set.add("c::1233");
    when(socketClient.isChannelOpen()).thenReturn(true);
    unsubscribeBetPackListener.onData(socketClient, Arrays.asList(data), ackSender);
    assertNotNull(data);
  }

  @Test
  void onDataFalse() throws Exception {
    String data = "222211218";
    AckRequest ackSender = null;
    when(socketClient.isChannelOpen()).thenReturn(false);
    when(socketClient.getHandshakeData()).thenReturn(handshakeData);
    unsubscribeBetPackListener.onData(socketClient, Arrays.asList(data), ackSender);
    assertNotNull(data);
  }
}
