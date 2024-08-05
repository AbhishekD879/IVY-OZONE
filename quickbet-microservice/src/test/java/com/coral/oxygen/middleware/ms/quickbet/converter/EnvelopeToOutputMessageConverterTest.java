package com.coral.oxygen.middleware.ms.quickbet.converter;

import static org.assertj.core.api.Assertions.assertThat;

import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Envelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.liveserv.OutputMessage;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.liveserv.Scoreboard;
import com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils;
import com.google.gson.Gson;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class EnvelopeToOutputMessageConverterTest {

  EnvelopeToOutputMessageConverter converter;

  @BeforeEach
  public void setUp() throws Exception {
    converter = new EnvelopeToOutputMessageConverter(new Gson());
  }

  @Test
  public void testConvertWithScoreboard() {
    Envelope envelope =
        new MessageEnvelope(
            "sEVENT0006820726",
            6820726,
            new Message(
                "MsEVENT0006820726!!!!!(8*M^GsEVENT0006820726000109000109",
                "{\"names\": {\"en\": \"PlayerA 1-2 PlayerB\"}}"));
    OutputMessage eventOutputMessage =
        TestUtils.deserializeWithGson(
            "converter/envelopeToOutputMessageConverter/sEVENT_message.json", OutputMessage.class);
    OutputMessage scbrdOutputMessage =
        TestUtils.deserializeWithGson(
            "converter/envelopeToOutputMessageConverter/sSCBRD_message.json", OutputMessage.class);
    Scoreboard scoreboard =
        TestUtils.deserializeWithGson(
            "converter/envelopeToOutputMessageConverter/scoreboard.json", Scoreboard.class);

    List<OutputMessage> messages = converter.convert(envelope);
    assertThat(messages).hasSize(2);
    assertThat(messages.get(0)).isEqualTo(eventOutputMessage);

    assertThat(messages.get(1).getChannel()).isEqualTo(scbrdOutputMessage.getChannel());
    assertThat(messages.get(1).getSubChannel()).isEqualTo(scbrdOutputMessage.getSubChannel());
    assertThat(messages.get(1).getEvent()).isEqualTo(scbrdOutputMessage.getEvent());
    assertThat(messages.get(1).getType()).isEqualTo(scbrdOutputMessage.getType());
    assertThat(messages.get(1).getMessage()).isEqualTo(scoreboard);
  }

  @Test
  public void testConvert() {
    Envelope envelope =
        new MessageEnvelope(
            "sEVENT0006820726",
            6820726,
            new Message(
                "MsEVENT0006820726!!!!!(8*M^GsEVENT0006820726000109000109",
                "{\"names\": {\"en\": \"PlayerA v PlayerB\"}}"));
    OutputMessage eventOutputMessage =
        TestUtils.deserializeWithGson(
            "converter/envelopeToOutputMessageConverter/sEVENT_message.json", OutputMessage.class);

    List<OutputMessage> messages = converter.convert(envelope);
    assertThat(messages).hasSize(2);
    assertThat(messages.get(0)).isEqualTo(eventOutputMessage);
  }
}
