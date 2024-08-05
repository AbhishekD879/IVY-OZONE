package com.ladbrokescoral.oxygen.listeners;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.listener.DataListener;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class ScoreboardUsunscribeListener implements DataListener<String> {
  @Override
  public void onData(SocketIOClient client, String eventId, AckRequest ackSender) throws Exception {
    if (client.isChannelOpen()) {
      client.leaveRoom(eventId);
    } else {
      log.info("Client got disconected with IP:{}", client.getHandshakeData().getAddress());
      client.disconnect();
    }
  }
}
