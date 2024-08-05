package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.*;
import static org.mockito.Matchers.any;
import static org.mockito.Mockito.*;

import com.egalacoral.spark.siteserver.api.*;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.TimelineSpotlightController;
import com.ladbrokescoral.oxygen.cms.api.entity.SpotlightEvents;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.spotlight.SpotlightEventInfo;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class TimelineSpotlightServiceTest {
  public static final String OUTCOME_ID = "123";
  public static final int RUNNER_NUMBER = 5;
  private TimelineSpotlightService service;

  @Mock SiteServeApiProvider siteServeApiProvider;
  @Mock SpotlightApiClient spotlightApiClient;

  @Mock SiteServerApi siteServerApi;

  List<Event> events;

  public static final String TYPE_ID_1 = "1";
  public static final String TYPE_ID_2 = "2";
  public static final String EV_ID_1 = "4242";
  public static final String EV_ID_2 = "5335";
  public static final String EV_ID_3 = "7868";
  public static final String TYPE_NAME_1 = "football";
  public static final String TYPE_NAME_2 = "basketball";

  public static final List<String> classIds =
      new ArrayList<String>() {
        {
          add("3");
          add("5");
          add("1");
        }
      };

  @Before
  public void setUp() {
    service = new TimelineSpotlightService(siteServeApiProvider, spotlightApiClient);

    when(siteServerApi.getEventToOutcomeForClass(
            anyList(),
            any(SimpleFilter.class),
            any(LimitToFilter.class),
            any(ExistsFilter.class),
            anyList()))
        .thenReturn(Optional.empty());

    Outcome outcome = new Outcome();
    outcome.setId(OUTCOME_ID);
    outcome.setRunnerNumber(RUNNER_NUMBER);

    Children outcomeContainer = new Children();
    outcomeContainer.setOutcome(outcome);

    Children marketContainer = new Children();
    marketContainer.setMarket(new Market());
    marketContainer.getMarket().setChildren(Arrays.asList(outcomeContainer));

    Children eventContainer = new Children();
    eventContainer.setEvent(new Event());
    eventContainer.getEvent().setChildren(Arrays.asList(marketContainer));

    Optional<List<Children>> children = Optional.of(Arrays.asList(eventContainer));
    when(siteServerApi.getEventToOutcomeForEvent(
            anyList(), any(SimpleFilter.class), any(), anyList()))
        .thenReturn(children);

    when(siteServeApiProvider.api(anyString())).thenReturn(siteServerApi);
  }

  @Test
  public void testReturningNullIfFetchedNullDataFromSiteServe() {
    TimelineSpotlightController.RefreshSiteserveEventsQuery query =
        new TimelineSpotlightController.RefreshSiteserveEventsQuery();
    query.setRefreshEventsClassesString("3, 5, 1");
    query.setRefreshEventsFrom(Instant.parse("2020-03-17T10:00:23.000Z"));
    query.setRestrictToUkAndIre(false);

    SpotlightEvents spotlightEvents = service.fetchSiteServeDataForBrandByApi("ladbrokes", query);

    assertEquals(null, spotlightEvents);
  }

  @Test
  public void testFetchingDataFromSiteserveCalledWithRightParams() {
    returnArrayOfEventsFromSiteServe();
    TimelineSpotlightController.RefreshSiteserveEventsQuery query =
        new TimelineSpotlightController.RefreshSiteserveEventsQuery();
    query.setRefreshEventsClassesString("3, 5, 1");
    query.setRefreshEventsFrom(Instant.parse("2020-03-17T10:00:23.000Z"));
    query.setRestrictToUkAndIre(false);

    service.fetchSiteServeDataForBrandByApi("ladbrokes", query);

    ArgumentCaptor<SimpleFilter> simpleFilterCaptor = ArgumentCaptor.forClass(SimpleFilter.class);
    ArgumentCaptor<List> classIdsCaptor = ArgumentCaptor.forClass(List.class);
    verify(siteServerApi, times(1))
        .getEventToOutcomeForClass(
            classIdsCaptor.capture(),
            simpleFilterCaptor.capture(),
            any(LimitToFilter.class),
            any(ExistsFilter.class),
            anyList());
    SimpleFilter actualSimpleFilter = simpleFilterCaptor.getValue();
    List classIdsActual = classIdsCaptor.getValue();
    assertEquals(classIds, classIdsActual);
    assertEquals(constructSimpleFilter(), actualSimpleFilter);
  }

  @Test
  public void testEventsFilteringAndGrouping() {
    returnArrayOfEventsFromSiteServe();
    TimelineSpotlightController.RefreshSiteserveEventsQuery query =
        new TimelineSpotlightController.RefreshSiteserveEventsQuery();
    query.setRefreshEventsClassesString("3, 5, 1");
    query.setRefreshEventsFrom(Instant.now());

    SpotlightEvents spotlightEvents = service.fetchSiteServeDataForBrandByApi("ladbrokes", query);

    List<SpotlightEvents.TypeEvent> expectedTypeEvents =
        Arrays.asList(
            new SpotlightEvents.TypeEvent(
                TYPE_ID_1, TYPE_NAME_1, Arrays.asList(eventById(EV_ID_1))),
            new SpotlightEvents.TypeEvent(
                TYPE_ID_2, TYPE_NAME_2, Arrays.asList(eventById(EV_ID_2))));
    assertEquals(expectedTypeEvents, spotlightEvents.getTypeEvents());
  }

  @Test
  public void testFetchingSpotlightDataForEventId() {
    String brand = "ladbrokes";
    String eventId = "23443";

    SpotlightEventInfo spotlightEventInfo = new SpotlightEventInfo();
    spotlightEventInfo.setHorses(new ArrayList<>());
    SpotlightEventInfo.HorseInfo horseInfo = new SpotlightEventInfo.HorseInfo();
    horseInfo.setHorseName("Flash");
    horseInfo.setSaddle(RUNNER_NUMBER + "");
    spotlightEventInfo.getHorses().add(horseInfo);
    when(spotlightApiClient.fetchSpotlightByEventId(brand, eventId)).thenReturn(spotlightEventInfo);

    service.fetchSpotlightData(brand, eventId);

    verify(spotlightApiClient).fetchSpotlightByEventId(brand, eventId);
    verify(siteServerApi)
        .getEventToOutcomeForEvent(anyList(), any(SimpleFilter.class), any(), anyList());
  }

  private SimpleFilter constructSimpleFilter() {
    SimpleFilter simpleFilter =
        (SimpleFilter)
            new SimpleFilter.SimpleFilterBuilder()
                .addBinaryOperation("event.siteChannels", BinaryOperation.contains, "M")
                .addUnaryOperation("event.isStarted", UnaryOperation.isFalse)
                .addBinaryOperation(
                    "market.templateMarketName", BinaryOperation.equals, "|Win or Each Way|")
                .addBinaryOperation(
                    "event.startTime", BinaryOperation.greaterThan, "2020-03-17T10:00:00Z")
                .addBinaryOperation(
                    "event.startTime", BinaryOperation.lessThan, "2020-03-17T22:00:23Z")
                .addUnaryOperation("event.isResulted", UnaryOperation.isFalse)
                .build();
    return simpleFilter;
  }

  private Event eventById(String eventId) {
    return this.events.stream()
        .filter(event -> event.getId().equals(eventId))
        .collect(Collectors.toList())
        .get(0);
  }

  private void returnArrayOfEventsFromSiteServe() {
    events = new ArrayList<>();
    Event event = new Event();
    event.setId(EV_ID_1);
    event.setTypeId(TYPE_ID_1);
    event.setTypeName(TYPE_NAME_1);
    event.setStartTime("2020-09-22T14:01:54.9571247Z");
    events.add(event);

    event = new Event();
    event.setId(EV_ID_2);
    event.setTypeId(TYPE_ID_2);
    event.setTypeName(TYPE_NAME_2);
    event.setStartTime("2020-09-22T15:01:54.9571247Z");
    events.add(event);

    event = new Event();
    event.setId(EV_ID_3);
    event.setTypeId(TYPE_ID_1);
    event.setTypeName(TYPE_NAME_1);
    event.setStartTime(null);
    events.add(event);

    when(siteServerApi.getEventToOutcomeForClass(
            anyList(),
            any(SimpleFilter.class),
            any(LimitToFilter.class),
            any(ExistsFilter.class),
            anyList()))
        .thenReturn(Optional.of(events));
  }
}
