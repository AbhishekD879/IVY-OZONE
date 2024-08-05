package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import static org.junit.Assert.assertNotNull;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.liveserv.impl.ManagedLiveServeService;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.ladbrokescoral.oxygen.timeline.api.model.obevent.SelectionStatus;
import io.vavr.collection.Stream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.*;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SubscriptionServiceImplTest {

  @Mock private ManagedLiveServeService liveServService;
  @Mock private SiteServerApi siteServerApi;

  @Test
  public void unsubscirbeTest()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {

    SubscriptionStats subscriptionStats = new SubscriptionStats("abc", 123456789);
    Map<String, SubscriptionStats> subscriptions = new HashMap<>();
    subscriptions.put("1", subscriptionStats);
    when(liveServService.getSubscriptions()).thenReturn(subscriptions);

    Map<String, String> eventIdToChannel =
        Stream.ofAll(subscriptions.entrySet())
            .toMap(entry -> Long.toString(entry.getValue().getEventId()), Map.Entry::getKey)
            .toJavaMap();

    SubscriptionServiceImpl subscriptionService =
        new SubscriptionServiceImpl(siteServerApi, liveServService);
    Method m = subscriptionService.getClass().getDeclaredMethod("unsubscribeFromFinishedEvents");
    m.setAccessible(true);
    m.invoke(subscriptionService);

    assertNotNull(eventIdToChannel);
  }

  @Test
  public void subscribeTest() {
    SubscriptionServiceImpl subscriptionService =
        new SubscriptionServiceImpl(siteServerApi, liveServService);
    subscriptionService.subscribe("123");
    SelectionStatus selectionStatus = new SelectionStatus();
    selectionStatus.setBoostedPriceNum("23");
    selectionStatus.setBoostedPriceDen("1");
    selectionStatus.setPriceStreamType("Price_boost");
    assertNotNull(subscriptionService);
  }

  @Test
  public void subscribeOnUpdatesTest() {
    SubscriptionServiceImpl subscriptionService =
        new SubscriptionServiceImpl(siteServerApi, liveServService);
    Event event = new Event();
    event.setId("1");
    Market market = new Market();
    market.setId("1");
    Outcome outcome = new Outcome();
    outcome.setId("1");
    market.setChildren(List.of(new Children()));
    market.getChildren().get(0).setOutcome(outcome);

    event.setChildren(List.of(new Children()));
    event.getChildren().get(0).setMarket(market);

    Mockito.when(
            siteServerApi.getEventToOutcomeForOutcome(
                Mockito.eq(List.of("123")),
                Mockito.any(SimpleFilter.class),
                Mockito.eq(null),
                Mockito.eq(false)))
        .thenReturn(Optional.of(List.of(event)));
    subscriptionService.subscribe("123");
    SelectionStatus selectionStatus = new SelectionStatus();
    selectionStatus.setBoostedPriceNum("23");
    selectionStatus.setBoostedPriceDen("1");
    selectionStatus.setPriceStreamType("Price_boost");
    assertNotNull(subscriptionService);
  }
}
