package com.oxygen.publisher.context;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import com.oxygen.publisher.model.TicksMetrics;
import lombok.extern.slf4j.Slf4j;

/** Created by Aliaksei Yarotski on 12/26/17. */
@Slf4j
public abstract class AbstractSessionContext {

  public static final String IO_SERVER_HEALTH_CHECK_ROOM_NAME = "IO_SERVER_HEALTH_CHECK";

  public abstract TicksMetrics getTicksMetrics();

  public abstract void registerListeners(SocketIOServer server);

  /**
   * Called on a new socket connection. Emits the application version and featured model structure.
   * Subscribes a relation to subscribed events.
   *
   * @param client the socket relation.
   */
  public abstract void onConnect(final SocketIOClient client);

  /**
   * Called on a socket disconnection. Unsubscribes the relation from all rooms.
   *
   * @param client the socket relation
   */
  @Trace(metricName = "Websocket/onDisconnect", dispatcher = true)
  public void onDisconnect(SocketIOClient client) {
    client.getAllRooms().forEach(client::leaveRoom);
    log.debug("Client disconnected {}", client.getSessionId());
    NewRelic.incrementCounter("Custom/onDisconnect");
  }

  /**
   * Warning: Socket IO protocol doesn't supported query parameters changing.
   *
   * @param client Socket.IO session representation
   * @return protocol version
   */
  public final String getProtocolVersion(SocketIOClient client) {
    return client.getHandshakeData().getSingleUrlParam("version");
  }

  public final String getModuleParam(SocketIOClient client) {
    return client.getHandshakeData().getSingleUrlParam("module");
  }

  public AbstractSocketEventListener getHealthCheckListener(final SocketIOServer server) {
    return new AbstractSocketEventListener<String>(IO_SERVER_HEALTH_CHECK_ROOM_NAME, String.class) {
      @Override
      public void onEventType(SocketIOClient socketIOClient, String data, AckRequest ackRequest) {

        int totalClients = server.getAllClients().size();

        log.info("### LIVE UPDATES COUNT = {} ####", getTicksMetrics().popLiveUpdatesTickCounter());
        log.info("### on SocketIO server connected {} clients. ####", totalClients);
        log.debug("Send health check response to {}", socketIOClient.getSessionId());
        socketIOClient.sendEvent(IO_SERVER_HEALTH_CHECK_ROOM_NAME, totalClients);
      }
    };
  }
}
