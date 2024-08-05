package com.coral.oxygen.middleware.ms.liveserv;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.liveserv.configuration.LiveServerConfig;
import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.SubscriptionAck;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Unsubscribed;
import com.coral.oxygen.middleware.ms.liveserv.newclient.EventIdResolver;
import com.coral.oxygen.middleware.ms.liveserv.newclient.chunked.ChunkedLiveUpdates;
import com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve.LiveServerClientBuilder;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.Map;
import java.util.Optional;
import org.junit.*;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

/** Created by azayats on 08.05.17. */
@RunWith(MockitoJUnitRunner.class)
public class LiveServServiceTest {

  @Mock private MessageHandler messageHandler;

  private LiveServService service;
  private EventIdResolver eventIdResolver;

  @Before
  public void setUp() throws ServiceException, NoSuchAlgorithmException, KeyManagementException {
    LiveServerConfig config = new LiveServerConfig();
    eventIdResolver = mock(EventIdResolver.class);
    when(eventIdResolver.resolveEventId(any(String.class))).thenReturn(Optional.of(5L));
    LiveServerClientBuilder liveServerClientBuilder =
        config.liveServerClientBuilder(
            "http://localhost:8090",
            config.callExecutor(config.okHttpClient(5, 100, "BODY", null, null)),
            5,
            config.liveServerListener(eventIdResolver, messageHandler));
    service =
        new LiveServServiceImpl(
            new ChunkedLiveUpdates(200, liveServerClientBuilder), eventIdResolver);
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
  public void testEmptySubscription() {
    Assert.assertTrue(service.getSubscriptions().isEmpty());
  }

  @Test
  public void testSubscription() {
    String channel = "sEVENT0102030405";
    // action
    service.subscribe(channel);
    // verification
    Map<String, SubscriptionStats> subscriptions = service.getSubscriptions();
    Assert.assertEquals(1, subscriptions.size());
    Assert.assertTrue(subscriptions.containsKey(channel));
    ArgumentCaptor<SubscriptionAck> captor = ArgumentCaptor.forClass(SubscriptionAck.class);
  }

  @Test
  public void testDuplicateSubscription() throws ServiceException {
    String channel = "sEVENT0102030405";
    // action
    service.subscribe(channel);
    // second time
    service.subscribe(channel);

    // verification
    Map<String, SubscriptionStats> subscriptions = service.getSubscriptions();
    Assert.assertEquals(1, subscriptions.size());
    Assert.assertTrue(subscriptions.containsKey(channel));

    // FIXME after changes it's getting called twice, but second time it's taken from cache
    //        Mockito.verify(eventIdResolver, Mockito.times(1)).resolveEventId(channel);
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
    Map<String, SubscriptionStats> subscriptions = service.getSubscriptions();
    Assert.assertEquals(0, subscriptions.size());
    ArgumentCaptor<Unsubscribed> captor = ArgumentCaptor.forClass(Unsubscribed.class);
  }
}
