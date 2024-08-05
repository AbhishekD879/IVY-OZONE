package com.gvc.oxygen.betreceipts.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Expired;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Unsubscribed;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.gvc.oxygen.betreceipts.liveserv.updates.EventMessageApplier;
import com.gvc.oxygen.betreceipts.service.EventService;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class EventMessageApplierTest implements WithAssertions {

  @Mock private LiveServService liveServService;

  @Mock private EventService eventService;

  @Spy private ObjectMapper objectMapper;

  @InjectMocks private EventMessageApplier eventMessageApplier;

  @Test
  void testHandleWithMessage() {
    MessageEnvelope messageEnvelope = getMessageEnvelope();
    Assertions.assertDoesNotThrow(() -> eventMessageApplier.applyUpdate(messageEnvelope));
  }

  @Test
  void testHandleWithMessageStartedFalse() {
    MessageEnvelope messageEnvelope = getMessageEnvelope();
    Assertions.assertDoesNotThrow(() -> eventMessageApplier.applyUpdate(messageEnvelope));
  }

  @Test
  void testHandleWithMessageForException() {
    MessageEnvelope messageEnvelope = getMessageEnvelope();
    messageEnvelope.getMessage().setJsonData(getMessageInvalid());
    Assertions.assertDoesNotThrow(() -> eventMessageApplier.applyUpdate(messageEnvelope));
  }

  @Test
  void testHandleWithMessageStarted() {
    MessageEnvelope messageEnvelope = getMessageEnvelope();
    messageEnvelope.getMessage().setJsonData(getMessageStartedFalse());
    Assertions.assertDoesNotThrow(() -> eventMessageApplier.applyUpdate(messageEnvelope));
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
    message.setJsonData(
        "{\"status\":\"A\",\"displayed\":\"Y\",\"result_conf\":\"Y\",\"started\":\"Y\"}");
    return message;
  }

  private String getMessageInvalid() {
    return "{\"status\":\"A\",\"displayed\":\"Y\",\"result_conf\":\"Y\",\"started\":\"Y\"";
  }

  private String getMessageStartedFalse() {
    return "{\"status\":\"A\",\"displayed\":\"Y\",\"result_conf\":\"Y\",\"started\":\"N\"}";
  }
}
