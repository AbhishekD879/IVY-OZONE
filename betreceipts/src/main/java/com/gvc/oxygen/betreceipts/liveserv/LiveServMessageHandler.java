package com.gvc.oxygen.betreceipts.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Envelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Expired;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.gvc.oxygen.betreceipts.liveserv.updates.LiveserveMessageApplierFactory;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

@Component
@Slf4j(topic = "liveserv")
public class LiveServMessageHandler implements MessageHandler {

  @Lazy @Autowired private LiveServService liveServService;

  private final LiveserveMessageApplierFactory liveserveMessageApplierFactory;

  public LiveServMessageHandler(
      @Lazy LiveServService liveServService,
      LiveserveMessageApplierFactory liveserveMessageApplierFactory) {

    this.liveServService = liveServService;
    this.liveserveMessageApplierFactory = liveserveMessageApplierFactory;
  }

  @Override
  public void handle(Envelope envelope) {
    String channel = envelope.getChannel();
    switch (envelope.getType()) {
      case EXPIRED:
        long eventId = ((Expired) envelope).getEventId();
        log.info("Resubscribe to channel {}, event {} after expiration", channel, eventId);
        log.info("expired subscription {}", envelope);
        liveServService.subscribe(channel, eventId);
        break;
      case MESSAGE:
        MessageEnvelope messageEnvelope = (MessageEnvelope) envelope;
        log.info("message {}", messageEnvelope.getMessage());
        liveserveMessageApplierFactory
            .get(messageEnvelope.getChannel())
            .applyUpdate(messageEnvelope);
        break;
      default:
        log.info("default case envelop {}", envelope);
        break;
    }
  }
}
