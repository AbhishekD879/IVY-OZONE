package com.gvc.oxygen.betreceipts.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Expired;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Unsubscribed;
import com.gvc.oxygen.betreceipts.liveserv.updates.ChannelMessageApplier;
import com.gvc.oxygen.betreceipts.liveserv.updates.LiveserveMessageApplierFactory;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class LiveMessageHandlerTest {

  @Mock private LiveServService liveServService;

  @Mock private LiveserveMessageApplierFactory liveserveMessageApplierFactory;

  @Mock private ChannelMessageApplier channelMessageApplier;

  @InjectMocks private LiveServMessageHandler liveServMessageHandler;

  @Test
  void testHandleWithMessage() {
    Mockito.when(liveserveMessageApplierFactory.get(Mockito.any()))
        .thenReturn(channelMessageApplier);
    MessageEnvelope messageEnvelope = getMessageEnvelope();
    Assertions.assertDoesNotThrow(() -> liveServMessageHandler.handle(messageEnvelope));
  }

  @Test
  void testHandleWithUnsub() {
    Unsubscribed messageEnvelope = getUnsubscribeMessageEnvelop();
    Assertions.assertDoesNotThrow(() -> liveServMessageHandler.handle(messageEnvelope));
  }

  @Test
  void testHandleWithExpired() {
    Expired messageEnvelope = getExpired();
    Assertions.assertDoesNotThrow(() -> liveServMessageHandler.handle(messageEnvelope));
  }

  private MessageEnvelope getMessageEnvelope() {
    return new MessageEnvelope("sEVENT993420000", 2233445, getMessage());
  }

  private Unsubscribed getUnsubscribeMessageEnvelop() {
    return new Unsubscribed("sEVENT993420000", 2233445);
  }

  private Expired getExpired() {
    return new Expired("sEVENT993420000", 2233445);
  }

  private Message getMessage() {
    Message message = new Message();
    message.setMessageCode("code1");
    message.setJsonData("{eventId:\"2233555\"}");
    return message;
  }
}
