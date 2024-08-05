package com.coral.oxygen.middleware.featured.service.injector;

import static java.util.stream.Collectors.toMap;
import static org.apache.commons.lang3.BooleanUtils.isNotTrue;

import com.coral.oxygen.middleware.common.mappers.EventMapper;
import com.coral.oxygen.middleware.common.service.DateTimeHelper;
import com.coral.oxygen.middleware.common.service.ModuleAdapter;
import com.coral.oxygen.middleware.common.service.featured.IdsCollector;
import com.coral.oxygen.middleware.common.utils.QueryFilterBuilder;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.*;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;
import org.joda.time.DateTime;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

@Component
@Slf4j
public class EventDataInjector extends ModuleAdapter implements EventsModuleInjector {
  private final SiteServerApi siteServerAPI;
  private final EventMapper eventMapper;
  private final QueryFilterBuilder queryFilterBuilder;
  private final DateTimeHelper dateTimeHelper;
  private static final String TWO_UP_MARKET = "2UpMarket";
  private static final String PRIMARY = "PrimaryMarket";
  private final String twoUpResultString;

  @Autowired
  public EventDataInjector(
      @Qualifier("featured") EventMapper eventMapper,
      SiteServerApi siteServerAPI,
      QueryFilterBuilder queryFilterBuilder,
      DateTimeHelper dateTimeHelper,
      @Value("${market.template.twoUpResult}") String twoUpResultString) {
    this.siteServerAPI = siteServerAPI;
    this.queryFilterBuilder = queryFilterBuilder;
    this.dateTimeHelper = dateTimeHelper;
    this.eventMapper = eventMapper;
    this.twoUpResultString = twoUpResultString;
  }

  public void injectData(List<? extends EventsModuleData> items, IdsCollector idsCollector) {
    // implemting two up markek  only for HightLightCoursel.current method is the invoked from all
    // modules except the HighlightCourosels.so default  it should be PRIMARY
    Map<String, Event> eventsMap = getIdEventMap(idsCollector, PRIMARY);
    mapEvents(items, eventsMap);
  }

  private void mapEvents(List<? extends EventsModuleData> items, Map<String, Event> eventsMap) {
    items.stream()
        .filter(d -> d.getId() != null)
        .filter(d -> d.getOutcomeId() == null) // only whole events should be processed here
        .filter(d -> eventsMap.containsKey(String.valueOf(d.getId())))
        .forEach(d -> eventMapper.map(d, eventsMap.get(String.valueOf(d.getId()))));
  }

  public void injectData(
      List<? extends EventsModuleData> items, IdsCollector idsCollector, String displayMarketType) {
    Map<String, Event> eventsMap = getIdEventMap(idsCollector, displayMarketType);
    mapEvents(items, eventsMap);
  }

  private Map<String, Event> getIdEventMap(IdsCollector idsCollector, String displayMarketType) {
    Collection<Long> eventsIds = idsCollector.getEventsIds();
    Collection<Long> enhMultiplesIds = idsCollector.getEnhMultiplesIds();
    List<Event> events = new ArrayList<>();
    if (!eventsIds.isEmpty()) {
      events = consumeEvents(eventsIds, displayMarketType);
    }
    if (!idsCollector.getOutrightEventIds().isEmpty()) {
      events.addAll(consumeOutrightEvents(idsCollector.getOutrightEventIds()));
    }
    if (!CollectionUtils.isEmpty(idsCollector.getMarketIds())) {
      events.addAll(consumeByMarketIds(idsCollector.getMarketIds()));
    }
    consumeTwoUpMarkekIfAvaliable(displayMarketType, events);
    Map<String, Event> eventsMap =
        events.stream().collect(Collectors.toMap(Event::getId, Function.identity(), (a, b) -> a));

    Map<String, Event> enhancedMultiples =
        consumeEnhanceMultiplesEvents(enhMultiplesIds).stream()
            .filter(Objects::nonNull)
            .collect(toMap(Event::getId, Function.identity()));
    eventsMap.putAll(enhancedMultiples);

    return eventsMap;
  }

  private List<Event> consumeByMarketIds(Collection<String> marketIds) {
    List<Event> events =
        siteServerAPI
            .getWholeEventToOutcomeForMarket(String.join(",", marketIds), false)
            .orElse(Collections.emptyList());

    return events.stream()
        .filter(event -> isNotTrue(event.getIsResulted()) && isNotSuspended(event))
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private boolean isNotSuspended(Event event) {
    return Objects.isNull(event.getSuspendAtTime())
        || DateTime.parse(event.getSuspendAtTime())
            .isAfter(dateTimeHelper.nowTrimmedToTenSeconds());
  }

  private List<Event> consumeEvents(Collection<Long> eventsIds, String displayMarketType) {
    SimpleFilter footballEventsFilter =
        queryFilterBuilder.getFilterForFootballEvents(displayMarketType);
    Optional<List<Children>> footballEvents =
        getEventToOutcomeForEvent(eventsIds, footballEventsFilter);

    SimpleFilter nonFootballEventsFilter = queryFilterBuilder.getFilterForNonFootballEvents();
    Optional<List<Children>> noFootballEvents =
        getEventToOutcomeForEvent(eventsIds, nonFootballEventsFilter);

    List<Children> ssResponse = new ArrayList<>();
    footballEvents.ifPresent(ssResponse::addAll);
    noFootballEvents.ifPresent(ssResponse::addAll);

    return toEvents(ssResponse);
  }

  private Optional<List<Children>> getEventToOutcomeForEvent(
      Collection<Long> eventsIds, SimpleFilter simpleFilter) {
    List<String> eventIdsList =
        eventsIds.stream().map(Object::toString).collect(Collectors.toCollection(ArrayList::new));
    return siteServerAPI.getEventToOutcomeForEvent(
        eventIdsList, simpleFilter, null, new ArrayList<>());
  }

  private List<Event> toEvents(List<Children> ssResponse) {
    return ssResponse.stream()
        .map(Children::getEvent)
        .filter(Objects::nonNull)
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private List<Event> consumeOutrightEvents(Collection<Long> eventsIds) {
    Optional<List<Children>> events =
        getEventToOutcomeForEvent(eventsIds, queryFilterBuilder.getFilterForOutrightEvents());
    return toEvents(events.orElse(Collections.emptyList()));
  }

  private List<Event> consumeEnhanceMultiplesEvents(Collection<Long> enhMultiplesIds) {
    Optional<List<Children>> events =
        getEventToOutcomeForEvent(
            enhMultiplesIds, queryFilterBuilder.getFilterForNotStartedEvents());
    return toEvents(events.orElse(Collections.emptyList()));
  }
  // 2 up is enable in CMS then need to check 2 up market in siteservecall if not available then
  // need to show matchresult or any
  private void consumeTwoUpMarkekIfAvaliable(String displayMarketType, List<Event> events) {
    if (!TWO_UP_MARKET.equals(displayMarketType)) return;
    List<String> twoUpmarkets =
        Arrays.stream(twoUpResultString.split(","))
            .flatMap(n -> Stream.of("|" + n + "|", n))
            .collect(Collectors.toCollection(ArrayList::new));
    Predicate<Children> is2upMarketPresent =
        marketChildren -> twoUpmarkets.contains(marketChildren.getMarket().getName());
    events.forEach(
        event ->
            event.getChildren().stream()
                .filter(is2upMarketPresent)
                .findFirst()
                .ifPresent(twoUpMarket -> event.setChildren(Arrays.asList(twoUpMarket))));
  }
}
