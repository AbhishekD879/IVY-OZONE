package com.coral.oxygen.middleware.ms.liveserv.impl;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;
import com.coral.oxygen.middleware.ms.liveserv.model.ChannelType;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SiteServEventIdResolverTest {

  @Mock SiteServerApi siteServerApi;

  private SiteServEventIdResolver siteServEventIdResolver;

  @Before
  public void setUp() {
    this.siteServEventIdResolver = new SiteServEventIdResolver(siteServerApi);
  }

  @Test
  public void testResolveByMarketId() throws ServiceException {
    String marketId = "123456";
    Market market = new Market();
    market.setId(marketId);
    market.setEventId("555555");
    List<Market> list = Collections.singletonList(market);
    Optional<List<Market>> ol = Optional.of(list);
    when(siteServerApi.getEventToOutcomeForMarket(marketId, false, true)).thenReturn(ol);

    long id = siteServEventIdResolver.resolve(ChannelType.SEVMKT, 123456);

    assertEquals(Long.parseLong(market.getEventId()), id);
  }

  @Test
  public void testEventsForMarketNotPresent() {
    // given
    String marketId = "123456";
    Optional<List<Market>> ol = Optional.empty();
    when(siteServerApi.getEventToOutcomeForMarket(marketId, false, true)).thenReturn(ol);

    // when
    ServiceException thrown =
        assertThrows(
            "Expected siteServEventIdResolver.resolve to throw, but it didn't",
            ServiceException.class,
            () -> siteServEventIdResolver.resolve(ChannelType.SEVMKT, 123456));

    // then
    assertEquals("Event for market 123456 not found.", thrown.getMessage());
  }

  @Test
  public void testEmptyEventsForMarket() {
    String marketId = "123456";
    List<Market> list = Collections.emptyList();
    Optional<List<Market>> ol = Optional.of(list);
    when(siteServerApi.getEventToOutcomeForMarket(marketId, false, true)).thenReturn(ol);

    // when
    ServiceException thrown =
        assertThrows(
            "Expected siteServEventIdResolver.resolve to throw, but it didn't",
            ServiceException.class,
            () -> siteServEventIdResolver.resolve(ChannelType.SEVMKT, 123456));

    // then
    assertEquals("Event for market 123456 not found.", thrown.getMessage());
  }

  @Test
  public void testWrongEventIdFormatForMarket() {
    String marketId = "123456";
    Market market = new Market();
    market.setId(marketId);
    market.setEventId("WRONG");
    List<Market> list = Collections.singletonList(market);
    Optional<List<Market>> ol = Optional.of(list);
    when(siteServerApi.getEventToOutcomeForMarket(marketId, false, true)).thenReturn(ol);

    // when
    ServiceException thrown =
        assertThrows(
            "Expected siteServEventIdResolver.resolve to throw, but it didn't",
            ServiceException.class,
            () -> siteServEventIdResolver.resolve(ChannelType.SEVMKT, 123456));

    // then
    assertEquals("Error parsing event id WRONG", thrown.getMessage());
  }

  @Test
  public void testResolveByOutcomeId() throws ServiceException {
    String outcomeId = "121212";
    Event event = new Event();
    event.setId("55555");
    List<Event> list = Collections.singletonList(event);
    Optional<List<Event>> events = Optional.of(list);

    when(siteServerApi.getEventToOutcomeForOutcome(
            eq(Collections.singletonList(outcomeId)),
            any(SimpleFilter.class),
            eq(Collections.emptyList())))
        .thenReturn(events);

    long id = siteServEventIdResolver.resolve(ChannelType.sSELCN, 121212);

    assertEquals(Long.parseLong(event.getId()), id);
  }

  @Test
  public void testEventsForOutcomeIdNotPresent() {
    String outcomeId = "121212";
    Optional<List<Event>> events = Optional.empty();

    when(siteServerApi.getEventToOutcomeForOutcome(
            eq(Collections.singletonList(outcomeId)),
            any(SimpleFilter.class),
            eq(Collections.emptyList())))
        .thenReturn(events);

    // when
    ServiceException thrown =
        assertThrows(
            "Expected siteServEventIdResolver.resolve to throw, but it didn't",
            ServiceException.class,
            () -> siteServEventIdResolver.resolve(ChannelType.sSELCN, 121212));

    // then
    assertEquals("Event for outcome 121212 not found.", thrown.getMessage());
  }

  @Test
  public void testEmptyEventsForOutcomeId() {

    String outcomeId = "121212";
    List<Event> list = Collections.emptyList();
    Optional<List<Event>> events = Optional.of(list);

    when(siteServerApi.getEventToOutcomeForOutcome(
            eq(Collections.singletonList(outcomeId)),
            any(SimpleFilter.class),
            eq(Collections.emptyList())))
        .thenReturn(events);

    // when
    ServiceException thrown =
        assertThrows(
            "Expected siteServEventIdResolver.resolve to throw, but it didn't",
            ServiceException.class,
            () -> siteServEventIdResolver.resolve(ChannelType.sSELCN, 121212));

    // then
    assertEquals("Event for outcome 121212 not found.", thrown.getMessage());
  }

  @Test
  public void testWrongEventIdFormatForOutcomeId() {
    String outcomeId = "121212";
    Event event = new Event();
    event.setId("WRONG");
    List<Event> list = Collections.singletonList(event);
    Optional<List<Event>> events = Optional.of(list);

    when(siteServerApi.getEventToOutcomeForOutcome(
            eq(Collections.singletonList(outcomeId)),
            any(SimpleFilter.class),
            eq(Collections.emptyList())))
        .thenReturn(events);

    // when
    ServiceException thrown =
        assertThrows(
            "Expected siteServEventIdResolver.resolve to throw, but it didn't",
            ServiceException.class,
            () -> siteServEventIdResolver.resolve(ChannelType.sSELCN, 121212));

    // then
    assertEquals("Error parsing event id WRONG", thrown.getMessage());
  }

  @Test
  public void testWrongChannel() {
    // when
    ServiceException thrown =
        assertThrows(
            "Expected siteServEventIdResolver.resolve to throw, but it didn't",
            ServiceException.class,
            () -> siteServEventIdResolver.resolve(ChannelType.sEVENT, 123456));

    // then
    assertEquals("Unsupported channel type sEVENT", thrown.getMessage());
  }
}
