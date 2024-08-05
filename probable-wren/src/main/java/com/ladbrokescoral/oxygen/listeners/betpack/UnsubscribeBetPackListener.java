package com.ladbrokescoral.oxygen.listeners.betpack;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.listener.DataListener;
import java.util.List;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class UnsubscribeBetPackListener implements DataListener<List<String>> {

  @Override
  public void onData(SocketIOClient client, List<String> data, AckRequest ackSender)
      throws Exception {
    if (client.isChannelOpen()) {
      data.forEach(client::leaveRoom);
      log.info("Were processed {} un-subscriptions for client {}", data, client.getSessionId());
    } else {
      log.info("Client got disconnected with IP:{}", client.getHandshakeData().getAddress());
      client.disconnect();
    }
  }
}
