package com.oxygen.publisher.context;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import lombok.Getter;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;

/** Created by Aliaksei Yarotski on 1/30/18. */
@Slf4j
public abstract class AbstractSocketEventListener<T> {

  @Getter private final String eventName;
  @Getter private final Class<T> eventClass;
  @Setter private SocketIOServer socketIOServer;

  public AbstractSocketEventListener(final String eventName, final Class<T> eventClass) {
    this.eventName = eventName;
    this.eventClass = eventClass;
  }

  public void registerListener(SocketIOServer server) {
    // Object.class parameter allows to avoid JsonMappingException on request parameters parsing
    server.addEventListener(eventName, Object.class, this::onEvent);
    this.socketIOServer = server;
  }

  public abstract void onEventType(SocketIOClient socketIOClient, T data, AckRequest ackRequest);

  // default behaviour for requests with missed data
  public void onEventType(SocketIOClient socketIOClient, AckRequest ackRequest) {
    onEventType(socketIOClient, null, ackRequest);
  }

  /**
   * Accept for Any type event.
   *
   * @param socketIOClient socket client
   * @param data incoming data
   * @param ackRequest N/A
   */
  private void onEvent(SocketIOClient socketIOClient, Object data, AckRequest ackRequest) {

    // valid business case
    if (data == null) {
      onEventType(socketIOClient, ackRequest);
    } else if (eventClass.isInstance(data)) {
      onEventType(socketIOClient, (T) data, ackRequest);
    } else {
      log.debug(
          String.format(
              "Unexpected request data type '%s', expected '%s' for event type '%s'.",
              data.getClass().getSimpleName(), eventClass.getSimpleName(), eventName));
    }
  }
}
