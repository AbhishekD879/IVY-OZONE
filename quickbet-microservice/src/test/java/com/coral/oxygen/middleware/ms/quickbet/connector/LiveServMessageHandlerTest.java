package com.coral.oxygen.middleware.ms.quickbet.connector;

import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Envelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.EnvelopeType;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Expired;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.liveserv.OutputChannel;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.liveserv.OutputMessage;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.liveserv.SimpleOutputMessage;
import com.coral.oxygen.middleware.ms.quickbet.converter.EnvelopeToOutputMessageConverter;
import com.coral.oxygen.middleware.ms.quickbet.converter.EnvelopeToSimpleOutputMessageConverter;
import com.corundumstudio.socketio.BroadcastOperations;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import io.vavr.collection.List;
import java.util.Collections;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class LiveServMessageHandlerTest {

  private static final String CHANNEL = "someChannel";

  @Mock private EnvelopeToSimpleOutputMessageConverter envToSimpleOutConverter;

  @Mock private EnvelopeToOutputMessageConverter envToOutConverter;

  @Mock private SocketIOServer logServer;

  @Mock private LiveServService liveServService;

  @InjectMocks private LiveServMessageHandler liveservMessageHandler;

  @Mock private BroadcastOperations broadcastOps;

  @BeforeEach
  void init() {
    when(logServer.getRoomOperations(any())).thenReturn(broadcastOps);
    liveservMessageHandler.setLiveServService(liveServService);
  }

  @Test
  void handleError() {
    // given
    Envelope envelope = createEnvelope(EnvelopeType.ERROR);

    SimpleOutputMessage outMsg = new SimpleOutputMessage();
    when(envToSimpleOutConverter.convert(envelope)).thenReturn(outMsg);

    // when
    liveservMessageHandler.handle(envelope);

    // then
    verify(broadcastOps).sendEvent(CHANNEL, outMsg);
  }

  @Test
  void handleUnsubscribe() {
    // given
    Envelope envelope = createEnvelope(EnvelopeType.UNSUBSCRIBE);

    SimpleOutputMessage outMsg = new SimpleOutputMessage();
    when(envToSimpleOutConverter.convert(envelope)).thenReturn(outMsg);

    // when
    liveservMessageHandler.handle(envelope);

    // then
    verify(broadcastOps).sendEvent(CHANNEL, outMsg);
  }

  @Test
  void handleExpiredWithClientsWaiting() {
    // given
    Expired envelope = new Expired("channelExpired", 12345L);
    when(broadcastOps.getClients()).thenReturn(Collections.singleton(mock(SocketIOClient.class)));
    // when
    liveservMessageHandler.handle(envelope);
    // then
    verify(liveServService).subscribe(envelope.getChannel(), envelope.getEventId());
  }

  @Test
  void handleExpiredWithNoClients() {
    // given
    Expired envelope = new Expired("channelExpired", 12345L);
    when(broadcastOps.getClients()).thenReturn(Collections.emptyList());
    // when
    liveservMessageHandler.handle(envelope);
    // then
    verifyNoInteractions(liveServService);
  }

  @Test
  void handleMessage() {
    // given
    Envelope envelope = createEnvelope(EnvelopeType.MESSAGE);

    OutputMessage msg1 = new OutputMessage();
    OutputChannel channel1 = new OutputChannel("someChannel1", 1, "type1");
    msg1.setChannel(channel1);

    OutputMessage msg2 = new OutputMessage();
    OutputChannel channel2 = new OutputChannel("someChannel2", 2, "type2");
    msg2.setChannel(channel2);

    when(envToOutConverter.convert(envelope)).thenReturn(List.of(msg1, msg2).asJava());

    // when
    liveservMessageHandler.handle(envelope);

    // then
    verify(broadcastOps).sendEvent(eq("someChannel1"), eq(msg1));
    verify(broadcastOps).sendEvent(eq("someChannel2"), eq(msg2));
  }

  @Test
  void handleSubscriptionError() {
    // given
    Envelope envelope = createEnvelope(EnvelopeType.SUBSCRIPTION_ERROR);

    SimpleOutputMessage outMsg = new SimpleOutputMessage();
    when(envToSimpleOutConverter.convert(envelope)).thenReturn(outMsg);

    SocketIOClient client1 = mock(SocketIOClient.class);
    SocketIOClient client2 = mock(SocketIOClient.class);
    when(broadcastOps.getClients()).thenReturn(List.of(client1, client2).asJava());

    // when
    liveservMessageHandler.handle(envelope);

    // then
    verify(broadcastOps).sendEvent(CHANNEL, outMsg);
    verify(client1).leaveRoom(CHANNEL);
    verify(client2).leaveRoom(CHANNEL);
  }

  private Envelope createEnvelope(EnvelopeType type) {
    Envelope envelope = mock(Envelope.class);
    when(envelope.getChannel()).thenReturn(CHANNEL);
    when(envelope.getType()).thenReturn(type);
    return envelope;
  }
}
