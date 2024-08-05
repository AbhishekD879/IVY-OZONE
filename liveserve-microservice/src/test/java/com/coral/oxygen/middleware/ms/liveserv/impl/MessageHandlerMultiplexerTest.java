package com.coral.oxygen.middleware.ms.liveserv.impl;

import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.EventMessageEnvelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.SubscriptionAck;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

/** Created by azayats on 08.05.17. */
public class MessageHandlerMultiplexerTest {

  private MessageHandlerMultiplexer multiplexer;

  private EventMessageEnvelope envelope;

  private MessageHandler messageHandler1;
  private MessageHandler messageHandler2;

  @Before
  public void setUp() {
    envelope = new SubscriptionAck("sEVENT0102030405", 1L);
    multiplexer = new MessageHandlerMultiplexer();
    messageHandler1 = Mockito.mock(MessageHandler.class);
    messageHandler2 = Mockito.mock(MessageHandler.class);
    multiplexer.addMessageHandler(messageHandler1);
    multiplexer.addMessageHandler(messageHandler2);
  }

  @After
  public void tearDown() {
    multiplexer = null;
    envelope = null;
    messageHandler2 = null;
    messageHandler1 = null;
  }

  @Test
  public void testDelegate() {
    multiplexer.handle(envelope);

    Mockito.verify(messageHandler1).handle(envelope);
    Mockito.verify(messageHandler2).handle(envelope);
  }
}
