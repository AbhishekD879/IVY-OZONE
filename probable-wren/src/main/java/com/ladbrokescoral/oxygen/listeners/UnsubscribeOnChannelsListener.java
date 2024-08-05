package com.ladbrokescoral.oxygen.listeners;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.listener.DataListener;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.util.List;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class UnsubscribeOnChannelsListener implements DataListener<List<String>> {

  @Trace(dispatcher = true)
  @Override
  public void onData(SocketIOClient client, List<String> data, AckRequest ackSender)
      throws Exception {
    if (client.isChannelOpen()) {
      NewRelic.setTransactionName(null, "unsubscribe");
      data.forEach(client::leaveRoom);
      log.debug("Were processed {} un-subscriptions for client {}", data, client.getSessionId());
    } else {
      log.info("Client got disconected with IP:{}", client.getHandshakeData().getAddress());
      client.disconnect();
    }
  }
}
