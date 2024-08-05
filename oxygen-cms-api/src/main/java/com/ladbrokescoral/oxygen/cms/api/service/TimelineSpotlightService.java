package com.ladbrokescoral.oxygen.cms.api.service;

import com.egalacoral.spark.siteserver.api.*;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.egalacoral.spark.siteserver.parameter.RacingForm;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.TimelineSpotlightController;
import com.ladbrokescoral.oxygen.cms.api.entity.SpotlightEvents;
import com.ladbrokescoral.oxygen.cms.api.entity.TypeFlagCodes;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.spotlight.SpotlightEventInfo;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.time.Duration;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class TimelineSpotlightService {
  public static final int SPOTLIGHT_EVENT_STARTTIME_HRS_OFFSET = 12;
  private final SiteServeApiProvider siteServeApiProvider;

  public static final String UK = "UK";
  public static final String IRE = "IRE";

  private SpotlightApiClient spotlightApiClient;

  public TimelineSpotlightService(
      SiteServeApiProvider siteServeApiProvider, SpotlightApiClient spotlightApiClient) {
    this.siteServeApiProvider = siteServeApiProvider;
    this.spotlightApiClient = spotlightApiClient;
  }

  public SpotlightEventInfo fetchSpotlightData(String brand, String eventId) {
    SpotlightEventInfo spotlightEventInfo =
        this.spotlightApiClient.fetchSpotlightByEventId(brand, eventId);
    if (spotlightEventInfo.getHorses() != null) {
      Map<String, String> runnerNumberToSelectionId =
          this.fetchRunnerNumberToSelectionIdForEvent(brand, eventId);

      spotlightEventInfo
          .getHorses()
          .forEach(
              (SpotlightEventInfo.HorseInfo horse) -> {
                String saddleNumber = horse.getSaddle();
                if (saddleNumber != null) {
                  horse.setSelectionId(runnerNumberToSelectionId.get(saddleNumber));
                }
              });
    }

    return spotlightEventInfo;
  }

  public SpotlightEvents fetchSiteServeDataForBrandByApi(
      String brand, TimelineSpotlightController.RefreshSiteserveEventsQuery query) {

    SpotlightEvents siteServeRelatedEvents = null;
    Optional<List<Event>> events =
        this.requestSiteserveDataByApi(
            brand,
            query.getRefreshEventsFrom(),
            query.getRefreshEventsClassesString(),
            query.isRestrictToUkAndIre());

    if (events.isPresent()) {
      // GroupBy typeId
      Map<String, List<Event>> eventsByTypeIds =
          events.get().stream().collect(Collectors.groupingBy(Event::getTypeId));
      List<SpotlightEvents.TypeEvent> typeEvents =
          eventsByTypeIds.entrySet().stream()
              .map(
                  (Map.Entry<String, List<Event>> stringListEntry) ->
                      new SpotlightEvents.TypeEvent(
                          stringListEntry.getKey(),
                          stringListEntry.getValue().get(0).getTypeName(),
                          stringListEntry.getValue()))
              .collect(Collectors.toList());
      // Ordering by eventStartTime
      typeEvents.forEach(
          (SpotlightEvents.TypeEvent typeEvent) -> {
            typeEvent.setEvents(
                typeEvent.getEvents().stream()
                    .filter(event -> event.getStartTime() != null)
                    .collect(Collectors.toList()));
            Collections.sort(typeEvent.getEvents(), Comparator.comparing(Event::getStartTime));
          });
      siteServeRelatedEvents = new SpotlightEvents(brand, typeEvents);
    }

    return siteServeRelatedEvents;
  }

  public Optional<List<Event>> requestSiteserveDataByApi(
      String brand, Instant baseDateTime, String classIdsString, boolean isRestrictToUkAndIre) {
    List<String> classIds =
        Arrays.asList(classIdsString.split(",")).stream()
            .map(s -> s.trim())
            .collect(Collectors.toList());

    SimpleFilter.SimpleFilterBuilder simpleFilterBuilder =
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation("event.siteChannels", BinaryOperation.contains, "M")
            .addUnaryOperation("event.isStarted", UnaryOperation.isFalse)
            .addBinaryOperation(
                "market.templateMarketName", BinaryOperation.equals, "|Win or Each Way|")
            .addBinaryOperation(
                "event.startTime",
                BinaryOperation.greaterThan,
                baseDateTime.truncatedTo(ChronoUnit.MINUTES).toString())
            .addBinaryOperation(
                "event.startTime",
                BinaryOperation.lessThan,
                baseDateTime
                    .plus(Duration.ofHours(SPOTLIGHT_EVENT_STARTTIME_HRS_OFFSET))
                    .toString())
            .addUnaryOperation("event.isResulted", UnaryOperation.isFalse);
    if (isRestrictToUkAndIre) {
      simpleFilterBuilder =
          simpleFilterBuilder.addBinaryOperation(
              "event.typeFlagCodes",
              BinaryOperation.intersects,
              TypeFlagCodes.of(UK, IRE).toString());
    }
    SimpleFilter simpleFilter = (SimpleFilter) simpleFilterBuilder.build();
    LimitToFilter limitToFilter = new LimitToFilter.LimitToFilterBuilder().build();
    ExistsFilter existFilter = new ExistsFilter.ExistsFilterBuilder().build();

    return siteServeApiProvider
        .api(brand)
        .getEventToOutcomeForClass(
            classIds, simpleFilter, limitToFilter, existFilter, Collections.singletonList("event"));
  }

  public Map<String, String> fetchRunnerNumberToSelectionIdForEvent(String brand, String eventId) {

    SimpleFilter.SimpleFilterBuilder simpleFilterBuilder = new SimpleFilter.SimpleFilterBuilder();
    SimpleFilter simpleFilter = (SimpleFilter) simpleFilterBuilder.build();
    Optional<List<Children>> children =
        siteServeApiProvider
            .api(brand)
            .getEventToOutcomeForEvent(
                Collections.singletonList(eventId),
                simpleFilter,
                EnumSet.of(RacingForm.OUTCOME),
                Collections.singletonList("market"));

    return fillRunnerNumberToSelectionIdMap(children);
  }

  private Map<String, String> fillRunnerNumberToSelectionIdMap(
      Optional<List<Children>> maybeChildren) {
    Map<String, String> map = new HashMap<>();

    maybeChildren.ifPresent(
        children ->
            children.forEach(
                (Children eventContainer) -> {
                  Event event = eventContainer.getEvent();
                  if (event != null && event.getMarkets() != null) {
                    event
                        .getMarkets()
                        .forEach(
                            (Market market) -> {
                              if (market != null && market.getChildren() != null) {
                                market
                                    .getChildren()
                                    .forEach(
                                        (Children outcomeContainer) -> {
                                          Outcome outcome = outcomeContainer.getOutcome();
                                          if (outcome != null) {
                                            String selectionId = outcome.getId();
                                            Integer runnerNumber = outcome.getRunnerNumber();
                                            if (selectionId != null
                                                && runnerNumber != null
                                                && map.get(String.valueOf(runnerNumber)) == null) {
                                              // put the first occurrance
                                              map.put(String.valueOf(runnerNumber), selectionId);
                                            }
                                          }
                                        });
                              }
                            });
                  }
                }));

    return map;
  }
}
