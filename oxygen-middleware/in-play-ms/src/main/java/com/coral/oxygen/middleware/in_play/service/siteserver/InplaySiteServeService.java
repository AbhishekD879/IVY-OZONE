package com.coral.oxygen.middleware.in_play.service.siteserver;

import static com.coral.oxygen.middleware.common.utils.QueryFilterBuilder.*;
import static com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType.*;
import static com.coral.oxygen.middleware.pojos.model.output.PrimaryMarkets.*;
import static java.util.stream.Collectors.*;

import com.coral.oxygen.middleware.common.service.AbstractSiteServeService;
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.coral.oxygen.middleware.common.utils.QueryFilterBuilder;
import com.coral.oxygen.middleware.in_play.service.OutrightOutcomesFilter;
import com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType;
import com.coral.oxygen.middleware.pojos.model.output.PrimaryMarkets;
import com.egalacoral.spark.siteserver.api.*;
import com.egalacoral.spark.siteserver.model.Aggregation;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class InplaySiteServeService extends AbstractSiteServeService {

  private final OutrightOutcomesFilter topThreeOutrightOutcomesFilter;
  private static final List<PrimaryMarkets> SPROTS_WITH_PRIMARY_MARKETS =
      Arrays.asList(FOOTBALL, TENNIS, BASKETBALL, RUGBY_UNION, RUGBY_LEAGUE, AMERICAN_FB);
  private static final String HR_CATEGORY_CODE = "HORSE_RACING";
  private final QueryFilterBuilder queryFilterBuilder;

  private static final String VIRTUAL_SPORTS_CATEGORY_ID = "39";
  private static final String EVENT_CATEGORY_ID = "event.categoryId";
  private static final String EVENT_SITE_CHANNELS = "event.siteChannels";

  private static final String EVENT_IS_STARTED = "event.isStarted";

  private static final String EVENT_START_TIME = "event.startTime";

  private static final String EVENT_SORT_CODE = "event.eventSortCode";

  private static final String EVENT_IS_DISPLAYED = "event.isDisplayed";

  @Autowired
  public InplaySiteServeService(
      SiteServerApi siteServerApi,
      MarketTemplateNameService marketTemplateNameService,
      OutrightOutcomesFilter topThreeOutrightOutcomesFilter,
      QueryFilterBuilder queryFilterBuilder) {
    super(siteServerApi, marketTemplateNameService);
    this.topThreeOutrightOutcomesFilter = topThreeOutrightOutcomesFilter;
    this.queryFilterBuilder = queryFilterBuilder;
  }

  public List<Category> getClasses(Set<String> sportCategoryIds) {
    String mergedCategoryIds = String.join(",", sportCategoryIds);

    SimpleFilter simpleFilter = queryFilterBuilder.getClassSimpleFilter(mergedCategoryIds);
    ExistsFilter existsFilter = queryFilterBuilder.getClassExistingFilter();
    return siteServerApi.getClasses(simpleFilter, existsFilter).orElse(Collections.emptyList());
  }

  public List<Category> getClassesforVirtualHub() {
    SimpleFilter simpleFilter = queryFilterBuilder.getClassSimpleFilter(VIRTUAL_SPORTS_CATEGORY_ID);
    ExistsFilter existsFilter = getClassExistingFilterVirtuaHub();
    return siteServerApi.getClasses(simpleFilter, existsFilter).orElse(Collections.emptyList());
  }

  public List<Event> getEvents(PrimaryMarkets primaryMarketCategory, List<String> classIds) {
    List<Event> events =
        primaryMarketCategory == null
            ? getEventsForClassExcludeOutright(classIds)
            : getEventsForClassWithPrimaryMarkets(classIds, primaryMarketCategory);
    if (SPROTS_WITH_PRIMARY_MARKETS.contains(primaryMarketCategory)) {

      List<Event> liveNowEvents = getLiveNowEvents(classIds);
      Set<String> liveNowEventIds =
          liveNowEvents.stream().map(Event::getId).collect(Collectors.toSet());

      events.removeIf(event -> liveNowEventIds.contains(event.getId()));
      events.addAll(liveNowEvents);
    }

    return mergeEventsWithOutrightMarkets(events, getOutrightEvents(classIds));
  }

  private List<Event> getLiveNowEvents(List<String> classIds) {
    ExistsFilter existFilter = queryFilterBuilder.getEventToOutcomeForAllActiveMarkets();
    // empty limit
    LimitToFilter limitToFilter = new LimitToFilter.LimitToFilterBuilder().build();
    SimpleFilter simpleFilter = queryFilterBuilder.getLiveFootballEventToOutcomeForClassFilter();
    Optional<List<Event>> events =
        siteServerApi.getEventToOutcomeForClass(
            classIds, simpleFilter, limitToFilter, existFilter, Collections.singletonList("event"));
    return events.orElse(Collections.emptyList());
  }

  private static Instant nowUtcWithoutMillis() {
    return Instant.now().truncatedTo(ChronoUnit.SECONDS);
  }

  public List<Event> getVirtualEvents(List<String> classIds) {

    SimpleFilter.SimpleFilterBuilder liveEventsFilterBuilder =
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation(
                EVENT_CATEGORY_ID, BinaryOperation.equals, VIRTUAL_SPORTS_CATEGORY_ID)
            .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
            .addBinaryOperation(EVENT_SORT_CODE, BinaryOperation.equals, "MTCH")
            .addBinaryOperation(
                EVENT_START_TIME, BinaryOperation.lessThanOrEqual, nowUtcWithoutMillis())
            .addField(EVENT_IS_STARTED)
            .addField(EVENT_IS_DISPLAYED)
            .addUnaryOperation("event.isResulted", UnaryOperation.isFalse);

    ExistsFilter eventMarketIsAvailableFilter = new ExistsFilter.ExistsFilterBuilder().build();

    LimitToFilter limitToFilter = new LimitToFilter.LimitToFilterBuilder().build();

    return siteServerApi
        .getEventToOutcomeForClass(
            classIds,
            (SimpleFilter) liveEventsFilterBuilder.build(),
            limitToFilter,
            eventMarketIsAvailableFilter)
        .orElse(Collections.emptyList());
  }

  public List<Event> getEventsForClassWithPrimaryMarkets(
      List<String> classIds, PrimaryMarkets primaryMarketsCategory) {
    ExistsFilter existFilter = queryFilterBuilder.getEventToOutcomeForAllActiveMarkets();
    LimitToFilter limitToFilter = queryFilterBuilder.getLowestMarketDisplayOrderLimitFilter();
    SimpleFilter simpleFilter;
    if (HR_CATEGORY_CODE.equalsIgnoreCase(primaryMarketsCategory.name())) {
      simpleFilter =
          queryFilterBuilder.getLiveOrUpcomingEventToOutcomeByHRPrimMarket(
              marketTemplateNameService.asQuery(primaryMarketsCategory.getPrimaryMarkets()));
    } else {
      simpleFilter =
          queryFilterBuilder.getLiveOrUpcomingEventToOutcomeByPrimMarket(
              marketTemplateNameService.asQuery(primaryMarketsCategory.getPrimaryMarkets()));
    }
    Optional<List<Event>> eventsOptional =
        siteServerApi.getEventToOutcomeForClass(classIds, simpleFilter, limitToFilter, existFilter);
    Comparator<Market> primaryMarketComparator =
        Comparator.comparingInt(
            market -> getPrimaryMarketOrderIndex(primaryMarketsCategory, market));
    return eventsOptional
        .map(events -> sortMarkets(events, primaryMarketComparator))
        .orElse(new ArrayList<>());
  }

  public Map<String, Integer> getHRMarketsCountPerEventForClass(List<String> classIds) {
    SimpleFilter simpleFilter =
        queryFilterBuilder.getHRMarketCountForLiveOrUpcomingEventSimpleFilter();
    Optional<List<Aggregation>> aggregations =
        siteServerApi.getEventMarketsCountForClass(classIds, simpleFilter);
    return aggregations.orElse(Collections.emptyList()).stream()
        .collect(toMap(item -> String.valueOf(item.getRefRecordId()), Aggregation::getCount));
  }

  public Map<String, Integer> getMarketsCountPerEventForClass(List<String> classIds) {
    SimpleFilter simpleFilter =
        queryFilterBuilder.getMarketCountForLiveOrUpcomingEventSimpleFilter();
    Optional<List<Aggregation>> aggregations =
        siteServerApi.getEventMarketsCountForClass(classIds, simpleFilter);
    return aggregations.orElse(Collections.emptyList()).stream()
        .collect(toMap(item -> String.valueOf(item.getRefRecordId()), Aggregation::getCount));
  }

  private List<Event> sortMarkets(List<Event> events, Comparator<Market> primaryMarketComparator) {
    return events.stream()
        .peek(event -> event.getMarkets().sort(primaryMarketComparator))
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private int getPrimaryMarketOrderIndex(PrimaryMarkets primaryMarketsCategory, Market market) {
    return primaryMarketsCategory.getOrderIndex(
        marketTemplateNameService.getType(market.getName()));
  }

  private List<Event> getEventsForClassExcludeOutright(List<String> classIds) {
    ExistsFilter existFilter = queryFilterBuilder.getEventToOutcomeForClassExistingFilter(true);
    LimitToFilter limitToFilter = queryFilterBuilder.getLowestMarketDisplayOrderLimitFilter();
    SimpleFilter simpleFilter =
        queryFilterBuilder.getEventToOutcomeForClassFilterExcludeTemplate(
            marketTemplateNameService.asQuery(OUTRIGHT));
    Optional<List<Event>> events =
        siteServerApi.getEventToOutcomeForClass(classIds, simpleFilter, limitToFilter, existFilter);
    return events.orElse(new ArrayList<>());
  }

  private List<Event> getOutrightEvents(List<String> classIds) {
    ExistsFilter existFilter = queryFilterBuilder.getEventToOutcomeForClassExistingFilter(false);
    LimitToFilter limitToFilter = queryFilterBuilder.getLowestMarketDisplayOrderLimitFilter();
    SimpleFilter simpleFilter =
        queryFilterBuilder.getEventToOutcomeForClassFilterWithMarketTemlates(
            marketTemplateNameService.asQuery(Arrays.asList(OUTRIGHT, THREE_BALL_BETTING)));
    Optional<List<Event>> events =
        siteServerApi.getEventToOutcomeForClass(classIds, simpleFilter, limitToFilter, existFilter);
    List<Event> filteredEvents =
        events.map(this::filterEventsWithMarkets).orElse(new ArrayList<>());
    return topThreeOutrightOutcomesFilter.filterOutcomes(filteredEvents);
  }

  private List<Event> filterEventsWithMarkets(List<Event> events) {
    return events.stream()
        .filter(event -> !event.getChildren().isEmpty())
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private List<Event> mergeEventsWithOutrightMarkets(
      List<Event> events, List<Event> eventsWithOutrightMarkets) {
    List<Event> mergedEvents = new ArrayList<>(events);
    Map<String, Event> eventByIdMap =
        events.stream().collect(Collectors.toMap(Event::getId, Function.identity()));

    for (Event eventOutright : eventsWithOutrightMarkets) {
      if (eventByIdMap.containsKey(eventOutright.getId())) {
        Event event = eventByIdMap.get(eventOutright.getId());
        event
            .getChildren()
            .addAll(
                eventOutright.getChildren().stream()
                    .filter(children -> children.getMarket() != null)
                    .filter(
                        children ->
                            isMarketTemplateNameOneOf(
                                children.getMarket().getTemplateMarketName(),
                                OUTRIGHT,
                                THREE_BALL_BETTING))
                    .collect(Collectors.toCollection(ArrayList::new)));
      } else {
        mergedEvents.add(eventOutright);
      }
    }
    return mergedEvents;
  }

  private boolean isMarketTemplateNameOneOf(
      String templateMarketName, MarketTemplateType... marketTemplateTypes) {
    return Stream.of(marketTemplateTypes)
        .anyMatch(type -> marketTemplateNameService.containsName(type, templateMarketName));
  }
}
