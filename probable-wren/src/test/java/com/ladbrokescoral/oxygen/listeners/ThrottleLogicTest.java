package com.ladbrokescoral.oxygen.listeners;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

import com.corundumstudio.socketio.SocketIOClient;
import java.net.SocketAddress;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class ThrottleLogicTest {

  private static final int SUBSCRIPTION_LIMIT = 5; // usually 500
  @Mock SocketIOClient client;
  @Mock SocketAddress socketAddress;

  @BeforeEach
  private void init() {
    HashSet<String> set = new HashSet<>();
    set.add("sSELCN1284341238");
    when(client.getAllRooms()).thenReturn(set);
  }

  @Test
  void hackerDetected() {
    when(client.getRemoteAddress()).thenReturn(socketAddress);
    List<String> data =
        Arrays.asList(
            "sSELCN1284341242",
            "sEVMKT0397759520",
            "sSELCN1284341243",
            "sSELCN1284341244",
            "sEVMKT0397759521",
            "sSELCN1284341245",
            "sSELCN1284341246");
    ThrottleLogic throttleLogic = new ThrottleLogic(SUBSCRIPTION_LIMIT);
    assertTrue(throttleLogic.hackerDetected(client, data));
  }

  @Test
  void normalFlow() {
    List<String> data = Arrays.asList("sSELCN1284341242", "sEVMKT0397759520");
    ThrottleLogic throttleLogic = new ThrottleLogic(SUBSCRIPTION_LIMIT);
    assertFalse(throttleLogic.hackerDetected(client, data));
  }
}
