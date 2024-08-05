package com.coral.oxygen.middleware.ms.quickbet.converter;

import com.coral.oxygen.middleware.ms.liveserv.model.messages.Envelope;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.liveserv.SimpleOutputMessage;
import org.springframework.stereotype.Component;

@Component
public class EnvelopeToSimpleOutputMessageConverter
    extends BaseConverter<Envelope, SimpleOutputMessage> {

  @Override
  public SimpleOutputMessage populateResult(Envelope envelop, SimpleOutputMessage message) {
    message.setType(envelop.getType());
    message.setChannel(envelop.getChannel());
    message.setDescription(envelop.getDescription());
    return message;
  }

  @Override
  protected SimpleOutputMessage createTarget() {
    return new SimpleOutputMessage();
  }
}
