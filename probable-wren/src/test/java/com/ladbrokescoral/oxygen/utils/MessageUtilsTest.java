package com.ladbrokescoral.oxygen.utils;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.when;

import com.corundumstudio.socketio.SocketIOClient;
import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.dto.messages.Envelope;
import com.ladbrokescoral.oxygen.dto.messages.EnvelopeType;
import com.ladbrokescoral.oxygen.dto.messages.ErrorAsk;
import com.ladbrokescoral.oxygen.dto.messages.MessageObjectEnvelope;
import com.ladbrokescoral.oxygen.dto.messages.SubscriptionAck;
import com.ladbrokescoral.oxygen.dto.messages.SubscriptionError;
import com.ladbrokescoral.oxygen.dto.messages.UnsubscribedAsk;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.Optional;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class MessageUtilsTest {

  public static final String CHANNEL_NAME = "sSELCN1056886113";
  @Mock Envelope envelope;
  @Mock Envelope.MessageObject message;
  @Mock Gson gson;
  @Mock SocketIOClient socketIOClient;

  @Test
  void throwsExceptionWhileTryingInstantiate() {
    InvocationTargetException thrown =
        assertThrows(
            InvocationTargetException.class,
            () -> {
              Class<?> cl = Class.forName("com.ladbrokescoral.oxygen.utils.MessageUtils");
              Constructor<?> constructor = cl.getDeclaredConstructor();
              constructor.setAccessible(true);
              constructor.newInstance();
            });

    assertTrue(thrown.getTargetException() instanceof IllegalStateException);
    assertTrue(thrown.getTargetException().getMessage().equals("Utility class"));
  }

  @Test
  void testConvertMessageEnvelope() {
    when(envelope.getType()).thenReturn(EnvelopeType.MESSAGE);
    when(envelope.getMessage()).thenReturn(message);
    when(message.getMessageCode())
        .thenReturn("MsSELCN0986656413!!!!\\\"`Yg_iGsPRICE098665641300001e00001e");
    when(envelope.getChannel()).thenReturn(CHANNEL_NAME);

    Object obj = MessageUtils.convert(envelope, gson);
    assertThat(obj).isInstanceOf(MessageObjectEnvelope.class);
  }

  @Test
  void testConvertSubscribedEnvelope() {
    when(envelope.getType()).thenReturn(EnvelopeType.SUBSCRIBED);
    when(envelope.getChannel()).thenReturn(CHANNEL_NAME);

    Object obj = MessageUtils.convert(envelope, gson);
    assertThat(obj).isInstanceOf(SubscriptionAck.class);
  }

  @Test
  void testConvertUnsubscribeEnvelope() {
    when(envelope.getType()).thenReturn(EnvelopeType.UNSUBSCRIBE);
    when(envelope.getChannel()).thenReturn(CHANNEL_NAME);

    Object obj = MessageUtils.convert(envelope, gson);
    assertThat(obj).isInstanceOf(UnsubscribedAsk.class);
  }

  @Test
  void testConvertSubscriptionErrorEnvelope() {
    when(envelope.getType()).thenReturn(EnvelopeType.SUBSCRIPTION_ERROR);
    when(envelope.getChannel()).thenReturn(CHANNEL_NAME);

    Object obj = MessageUtils.convert(envelope, gson);
    assertThat(obj).isInstanceOf(SubscriptionError.class);
  }

  @Test
  void testConvertErrorEnvelope() {
    when(envelope.getType()).thenReturn(EnvelopeType.ERROR);

    Object obj = MessageUtils.convert(envelope, gson);
    assertThat(obj).isInstanceOf(ErrorAsk.class);
  }

  @Test
  void testToMessageObjectEnvelopeConversion() {
    when(envelope.getType()).thenReturn(EnvelopeType.MESSAGE);
    when(envelope.getMessage()).thenReturn(message);
    when(message.getMessageCode())
        .thenReturn("MsSELCN0986656413!!!!\\\"`Yg_iGsPRICE098665641300001e00001e");
    when(envelope.getChannel()).thenReturn(CHANNEL_NAME);

    Optional<MessageObjectEnvelope> message = MessageUtils.toMessage(envelope, gson);
    assertThat(message).isNotEmpty();
    assertThat(message.get().getType()).isEqualTo(EnvelopeType.MESSAGE);
    assertThat(message.get().getChannel().getType()).isEqualTo("sSELCN");
  }

  @Test
  void testToMessageObjectEnvelopeConversionOfOtherType() {
    when(envelope.getType()).thenReturn(EnvelopeType.ERROR);

    Optional message = MessageUtils.toMessage(envelope, gson);
    assertThat(message).isEmpty();
  }

  @Test
  void testNotifyExceptionHandling() {
    doThrow(RuntimeException.class).when(socketIOClient).sendEvent(any(), any());
    Assertions.assertDoesNotThrow(
        () -> {
          MessageUtils.notify("channel", null, socketIOClient, "transactionName");
        });
  }
}
