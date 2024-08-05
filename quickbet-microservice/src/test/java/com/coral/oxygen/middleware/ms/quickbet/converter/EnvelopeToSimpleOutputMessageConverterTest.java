package com.coral.oxygen.middleware.ms.quickbet.converter;

import static org.assertj.core.api.Assertions.assertThat;

import com.coral.oxygen.middleware.ms.liveserv.model.messages.Envelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.liveserv.SimpleOutputMessage;
import java.util.UUID;
import org.junit.jupiter.api.Test;

public class EnvelopeToSimpleOutputMessageConverterTest {

  @Test
  public void testSimpleConvert() {
    Envelope envelope = new MessageEnvelope(UUID.randomUUID().toString(), 0L, null);
    EnvelopeToSimpleOutputMessageConverter converter = new EnvelopeToSimpleOutputMessageConverter();

    SimpleOutputMessage outputMessage = converter.convert(envelope);
    assertThat(outputMessage.getChannel()).isEqualTo(envelope.getChannel());
    assertThat(outputMessage.getDescription()).isEqualTo(envelope.getDescription());
    assertThat(outputMessage.getType()).isEqualTo(envelope.getType());
  }
}
