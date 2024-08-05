package com.ladbrokescoral.oxygen.listeners;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.listener.DataListener;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class IncidentsListener implements DataListener<String> {

  private static final int SIX = 6;

  /**
   * Invokes when data object received from client
   *
   * @param client - receiver
   * @param obEventId - received object
   * @param ackSender - ack request
   * @throws Exception
   */
  @Override
  public void onData(SocketIOClient client, String obEventId, AckRequest ackSender)
      throws Exception {
    log.info("Starting to work with incidents eventId: {}", obEventId);
    String eventId = obEventId.substring(SIX);
    if (client.isChannelOpen()) {
      client.joinRoom(eventId);
    } else {
      log.info(
          "Client got disconected with Incidents IP:{}", client.getHandshakeData().getAddress());
      client.disconnect();
    }
  }
}
