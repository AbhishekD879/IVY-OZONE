package com.coral.oxygen.middleware.ms.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.client.Call;
import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;
import com.coral.oxygen.middleware.ms.liveserv.impl.EventIdResolver;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.ErrorMessage;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.SubscriptionAck;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.SubscriptionError;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Unsubscribed;
import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

/** Created by azayats on 08.05.17. */
@RunWith(MockitoJUnitRunner.class)
public class LiveServServiceImplTest {

  @Mock private MessageHandler messageHandler;

  @Mock private EventIdResolver eventIdResolver;

  @Mock private Call call;

  private LiveServService service;

  @Before
  public void setUp() throws ServiceException {
    Mockito.when(eventIdResolver.resolveEventId(Mockito.anyString())).thenReturn(5L);
    service =
        new LiveServeServiceFactory()
            .createSimpleLiveServeService(call, messageHandler, eventIdResolver);
  }

  @After
  public void tearDown() {
    service = null;
  }

  @Test(expected = NullPointerException.class)
  public void testSubscribeNullChannel() {
    service.subscribe(null);
  }

  @Test(expected = NullPointerException.class)
  public void testUnsubscribeNull() {
    service.unsubscribe(null);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testShorterChannel() {
    service.subscribe("sEVENT123456789");
  }

  @Test(expected = IllegalArgumentException.class)
  public void testLongerChannel() {
    service.subscribe("sEVENT12345678901");
  }

  @Test
  public void testSubscription() {
    String channel = "sEVENT0102030405";
    // action
    service.subscribe(channel);
    // verification
    ArgumentCaptor<SubscriptionAck> captor = ArgumentCaptor.forClass(SubscriptionAck.class);
    Mockito.verify(messageHandler).handle(captor.capture());
    SubscriptionAck message = captor.getValue();
    Assert.assertEquals(channel, message.getChannel());
    Assert.assertEquals(5L, message.getEventId());
  }

  @Test
  public void testDuplicateSubscription() throws ServiceException {
    String channel = "sEVENT0102030405";
    // action
    service.subscribe(channel);
    // second time
    service.subscribe(channel);

    // verification
    ArgumentCaptor<SubscriptionAck> captor = ArgumentCaptor.forClass(SubscriptionAck.class);
    Mockito.verify(messageHandler, Mockito.times(2)).handle(captor.capture());
    SubscriptionAck message = captor.getAllValues().get(1);
    Assert.assertEquals(channel, message.getChannel());
    Assert.assertEquals(5L, message.getEventId());
    // only one eventId resolving
    Mockito.verify(eventIdResolver, Mockito.times(1)).resolveEventId(channel);
  }

  @Test
  public void testSubscriptionWithEventIdResolvingFail() throws ServiceException {
    String channel = "sEVENT0102030405";
    // fail of resolving
    Mockito.doThrow(new ServiceException()).when(eventIdResolver).resolveEventId(channel);

    // action
    service.subscribe(channel);
    // verification
    ArgumentCaptor<SubscriptionError> captor = ArgumentCaptor.forClass(SubscriptionError.class);
    Mockito.verify(messageHandler).handle(captor.capture());
    SubscriptionError subscriptionError = captor.getValue();
    Assert.assertEquals(channel, subscriptionError.getChannel());
  }

  @Test
  public void tesUnsubscribeAftertDuplicateSubscription() throws ServiceException {
    String channel = "sEVENT0102030405";

    // first subscribe
    service.subscribe(channel);
    // second subscribe
    service.subscribe(channel);
    Mockito.reset(messageHandler);
    // unsubscribe
    service.unsubscribe(channel);

    // verification
    ArgumentCaptor<Unsubscribed> captor = ArgumentCaptor.forClass(Unsubscribed.class);
    Mockito.verify(messageHandler, Mockito.times(1)).handle(captor.capture());
    Unsubscribed message = captor.getValue();
    Assert.assertEquals(channel, message.getChannel());
    Assert.assertEquals(5L, message.getEventId());
  }

  @Test
  public void tesUnsubscribeWithoutSubscription() throws ServiceException {
    String channel = "sEVENT0102030405";

    // unsubscribe
    service.unsubscribe(channel);

    // verification
    ArgumentCaptor<ErrorMessage> captor = ArgumentCaptor.forClass(ErrorMessage.class);
    Mockito.verify(messageHandler, Mockito.times(1)).handle(captor.capture());
    ErrorMessage message = captor.getValue();
    Assert.assertEquals(channel, message.getChannel());
  }
}
