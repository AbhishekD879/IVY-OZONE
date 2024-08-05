package com.coral.oxygen.middleware.ms.quickbet.connector;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Envelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Expired;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.liveserv.OutputMessage;
import com.coral.oxygen.middleware.ms.quickbet.converter.EnvelopeToOutputMessageConverter;
import com.coral.oxygen.middleware.ms.quickbet.converter.EnvelopeToSimpleOutputMessageConverter;
import com.corundumstudio.socketio.SocketIOServer;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class LiveServMessageHandler implements MessageHandler {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  private final EnvelopeToSimpleOutputMessageConverter envelopeToSimpleOutputMessageConverter;
  private final EnvelopeToOutputMessageConverter envelopeToOutputMessageConverter;
  private final SocketIOServer socketIOServer;
  private LiveServService liveServService;

  @Lazy
  @Autowired
  public void setLiveServService(LiveServService liveServService) {
    this.liveServService = liveServService;
  }

  @Override
  public void handle(Envelope envelope) {
    String channel = envelope.getChannel();
    switch (envelope.getType()) {
      case EXPIRED:
        if (!socketIOServer.getRoomOperations(channel).getClients().isEmpty()) {
          long eventId = ((Expired) envelope).getEventId();
          ASYNC_LOGGER.info(
              "Resubscribe to channel {}, event {} after expiration", channel, eventId);
          liveServService.subscribe(channel, eventId);
        }
        break;
      case ERROR, UNSUBSCRIBE:
        socketIOServer
            .getRoomOperations(channel)
            .sendEvent(channel, envelopeToSimpleOutputMessageConverter.convert(envelope));
        break;
      case MESSAGE:
        List<OutputMessage> messages = envelopeToOutputMessageConverter.convert(envelope);
        messages.forEach(
            message -> {
              String messageChannel = message.getChannel().getName();
              socketIOServer.getRoomOperations(messageChannel).sendEvent(messageChannel, message);
            });
        break;
      case SUBSCRIPTION_ERROR:
        socketIOServer
            .getRoomOperations(channel)
            .sendEvent(channel, envelopeToSimpleOutputMessageConverter.convert(envelope));
        socketIOServer
            .getRoomOperations(channel)
            .getClients()
            .forEach(client -> client.leaveRoom(channel));
        break;
      default:
        break;
    }
  }
}
