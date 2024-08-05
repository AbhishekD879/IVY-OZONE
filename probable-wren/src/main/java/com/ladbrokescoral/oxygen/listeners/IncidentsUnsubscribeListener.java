package com.ladbrokescoral.oxygen.listeners;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.listener.DataListener;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class IncidentsUnsubscribeListener implements DataListener<String> {

  private static final int SIX = 6;

  /**
   * Unsuscribe/leave the room when data object received from client
   *
   * @param client
   * @param obEventId
   * @param ackSender
   * @throws Exception
   */
  @Override
  public void onData(SocketIOClient client, String obEventId, AckRequest ackSender)
      throws Exception {
    log.info("IncidentsUnsubscribeListener  onData {}", obEventId);
    if (client.isChannelOpen()) {
      String eventId = obEventId.substring(SIX);
      client.leaveRoom(eventId);
    } else {
      client.disconnect();
    }
  }
}
