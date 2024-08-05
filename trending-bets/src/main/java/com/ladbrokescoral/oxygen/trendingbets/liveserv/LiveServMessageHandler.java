package com.ladbrokescoral.oxygen.trendingbets.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Envelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.EnvelopeType;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.ladbrokescoral.oxygen.trendingbets.liveserv.updates.LiveserveMessageApplierFactory;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class LiveServMessageHandler implements MessageHandler {

  private final LiveserveMessageApplierFactory liveserveMessageApplierFactory;

  public LiveServMessageHandler(LiveserveMessageApplierFactory liveserveMessageApplierFactory) {

    this.liveserveMessageApplierFactory = liveserveMessageApplierFactory;
  }

  @Override
  public void handle(Envelope envelope) {

    if (EnvelopeType.MESSAGE.equals(envelope.getType())) {
      MessageEnvelope messageEnvelope = (MessageEnvelope) envelope;
      log.info("message {}", messageEnvelope.getMessage());
      liveserveMessageApplierFactory.get(messageEnvelope.getChannel()).applyUpdate(messageEnvelope);
    }
  }
}
