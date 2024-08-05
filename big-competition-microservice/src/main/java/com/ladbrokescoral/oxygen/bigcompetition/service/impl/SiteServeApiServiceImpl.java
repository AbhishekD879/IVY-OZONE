package com.ladbrokescoral.oxygen.bigcompetition.service.impl;

import static com.egalacoral.spark.siteserver.api.SiteServerImpl.EMPTY_EXISTS_FILTER;
import static com.ladbrokescoral.oxygen.bigcompetition.util.Utils.toStringList;

import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.LimitToFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.api.UnaryOperation;
import com.egalacoral.spark.siteserver.model.Aggregation;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.bigcompetition.service.SiteServeApiService;
import com.ladbrokescoral.oxygen.bigcompetition.util.Utils;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class SiteServeApiServiceImpl implements SiteServeApiService {

  private final SiteServerApi siteServerApi;

  private static final List<String> EVENT_MARKET_PRUNE_LIST = Arrays.asList("event", "market");

  @Value("${siteserve.market.template.knockoutEvents}")
  private String knockoutEventMarkets;

  @Value("${siteserve.market.template.nextEvents}")
  private String nextEventMarkets;

  @Value("${siteserver.priceboost.simplefilter.value}")
  private String hasPriceStreamValue;

  @Value("${siteserver.priceboost.enabled}")
  private boolean isPriceBoostEnabled;

  @Value("${siteserver.priceboost.simplefilter.key}")
  private String hasPriceStreamKey;

  @Override
  @Cacheable(value = "EventWithOutcomesForMarket")
  public Optional<Event> getEventWithOutcomesForMarket(String marketId) {
    Utils.newRelicLogTransaction("/SS-getWholeEventToOutcomeForMarket");
    return siteServerApi
        .getWholeEventToOutcomeForMarket(marketId, false)
        .map(List::stream)
        .flatMap(Stream::findFirst);
  }

  @Override
  @Cacheable(value = "EventWithOutcomesForEventSpecial")
  public List<Event> getEventWithOutcomesForEventSpecial(List<Integer> eventIds) {
    Utils.newRelicLogTransaction("/SS-getEventToOutcomeForEvent");
    return siteServerApi
        .getEventToOutcomeForEvent(
            toStringList(eventIds),
            getDefaultSimpleFilter(),
            getSpecialExistsFilter(),
            Arrays.asList("event", "market"),
            false)
        .orElseGet(ArrayList::new);
  }

  @Override
  @Cacheable(value = "EventWithOutcomesForEventKnockout")
  public Optional<Event> getEventWithOutcomesForEventKnockout(String eventId) {
    Utils.newRelicLogTransaction("/SS-getEventToOutcomeForEvent");

    LimitToFilter limitToFilter = getEventToOutcomeForTypeLimitFilter();
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addBinaryOperation(
        "market.templateMarketName", BinaryOperation.in, knockoutEventMarkets);
    builder.addPriceStream(hasPriceStreamKey, hasPriceStreamValue, isPriceBoostEnabled);
    return siteServerApi
        .getEventToOutcomeForEvent(
            Collections.singletonList(eventId),
            (SimpleFilter) builder.build(),
            EMPTY_EXISTS_FILTER,
            limitToFilter,
            EVENT_MARKET_PRUNE_LIST,
            false)
        .map(List::stream)
        .flatMap(Stream::findFirst);
  }

  @Override
  @Cacheable(value = "EventWithOutcomesForTypeSpecial")
  public List<Event> getEventWithOutcomesForTypeSpecial(List<Integer> typeIds) {
    Utils.newRelicLogTransaction("/SS-getEventToOutcomeForType");
    return siteServerApi
        .getEventToOutcomeForType(
            toStringList(typeIds),
            getDefaultSimpleFilter(),
            getSpecialExistsFilter(),
            Arrays.asList("event", "market"),
            false)
        .orElseGet(ArrayList::new);
  }

  @Override
  @Cacheable(value = "NextEventForType")
  public List<Event> getNextEventForType(Integer typeId) {

    List<String> arrayOfTypeId = Collections.singletonList(String.valueOf(typeId));

    SimpleFilter simpleFilter = getSimpleFilterForNextEventsByType();

    ExistsFilter existsFilter = getExistedFilterForNextEventsByType();

    LimitToFilter limitToFilter = getEventToOutcomeForTypeLimitFilter();

    List<String> arrayOfPrune = Collections.singletonList("event");

    boolean exclude = false;

    Utils.newRelicLogTransaction("/SS-getEventToOutcomeForType");
    return siteServerApi
        .getEventToOutcomeForType(
            arrayOfTypeId, simpleFilter, existsFilter, limitToFilter, arrayOfPrune, exclude)
        .orElseGet(ArrayList::new);
  }

  @Override
  @Cacheable(value = "NextEventForEvent")
  public List<Event> getNextEventForEvent(List<Integer> listOfEventId) {
    List<String> arrayOfEventId =
        listOfEventId.stream().distinct().map(String::valueOf).collect(Collectors.toList());

    SimpleFilter simpleFilter = getSimpleFilterForNextEventsByType();

    ExistsFilter existsFilter = getExistedFilterForNextEventsByType();

    LimitToFilter limitToFilter = getEventToOutcomeForTypeLimitFilter();

    List<String> arrayOfPrune = Collections.singletonList("event");

    boolean exclude = false;
    Utils.newRelicLogTransaction("/SS-getEventToOutcomeForEvent");
    return siteServerApi
        .getEventToOutcomeForEvent(
            arrayOfEventId, simpleFilter, existsFilter, limitToFilter, arrayOfPrune, exclude)
        .orElseGet(ArrayList::new);
  }

  @Override
  @Cacheable(value = "MarketsCountForEvents")
  public Optional<List<Aggregation>> getMarketsCountForEvents(List<Integer> listOfEventId) {
    SimpleFilter simpleFilter = getMarketCountEventForClassSimpleFilter();
    List<String> events =
        listOfEventId.stream().distinct().map(String::valueOf).collect(Collectors.toList());
    Utils.newRelicLogTransaction("/SS-getMarketsCountForEvent");
    return siteServerApi.getMarketsCountForEvent(events, simpleFilter);
  }

  @Override
  @Cacheable(value = "WholeEventToOutcomeForMarket")
  public Optional<List<Event>> getWholeEventToOutcomeForMarket(
      String marketIds, boolean showUndisplayed) {
    Utils.newRelicLogTransaction("/SS-getWholeEventToOutcomeForMarket");
    return siteServerApi.getWholeEventToOutcomeForMarket(marketIds, showUndisplayed);
  }

  @Override
  @Cacheable(value = "EventToOutcomeForMarkets")
  public Optional<List<Event>> getEventToOutcomeForMarkets(List<String> marketIds) {
    Utils.newRelicLogTransaction("/SS-getEventToOutcomeForMarkets");
    return siteServerApi.getWholeEventToOutcomeForMarket(marketIds, false);
  }

  private static SimpleFilter getMarketCountEventForClassSimpleFilter() {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addBinaryOperation("event.siteChannels", BinaryOperation.contains, "M");
    builder.addBinaryOperation("market.siteChannels", BinaryOperation.contains, "M");
    builder.addUnaryOperation("event.isStarted", UnaryOperation.isFalse);
    return (SimpleFilter) builder.build();
  }

  private SimpleFilter getDefaultSimpleFilter() {
    return (SimpleFilter)
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation("event.siteChannels", BinaryOperation.contains, "M")
            .addBinaryOperation(
                "event.suspendAtTime",
                BinaryOperation.greaterThanOrEqual,
                Instant.now().truncatedTo(ChronoUnit.MINUTES))
            .addPriceStream(hasPriceStreamKey, hasPriceStreamValue, isPriceBoostEnabled)
            .build();
  }

  private ExistsFilter getSpecialExistsFilter() {
    return (ExistsFilter)
        new ExistsFilter.ExistsFilterBuilder()
            .addBinaryOperation(
                "event:simpleFilter:market.drilldownTagNames",
                BinaryOperation.intersects,
                "MKTFLAG_SP")
            .build();
  }

  public SimpleFilter getSimpleFilterForNextEventsByType() {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addBinaryOperation("event.siteChannels", BinaryOperation.contains, "M");
    builder.addBinaryOperation("market.siteChannels", BinaryOperation.contains, "M");
    builder.addBinaryOperation("outcome.siteChannels", BinaryOperation.contains, "M");
    builder.addBinaryOperation("market.templateMarketName", BinaryOperation.in, nextEventMarkets);
    builder.addUnaryOperation("event.isStarted", UnaryOperation.isFalse);
    builder.addBinaryOperation(
        "event.suspendAtTime",
        BinaryOperation.greaterThan,
        Instant.now().truncatedTo(ChronoUnit.MINUTES));
    builder.addPriceStream(hasPriceStreamKey, hasPriceStreamValue, isPriceBoostEnabled);
    return (SimpleFilter) builder.build();
  }

  private ExistsFilter getExistedFilterForNextEventsByType() {
    ExistsFilter.ExistsFilterBuilder builder = new ExistsFilter.ExistsFilterBuilder();
    builder.addUnaryOperation("event:simpleFilter:market.isResulted", UnaryOperation.isFalse);
    builder.addField("event:simpleFilter:market.isDisplayed");
    return builder.build();
  }

  private LimitToFilter getEventToOutcomeForTypeLimitFilter() {
    LimitToFilter.LimitToFilterBuilder builder = new LimitToFilter.LimitToFilterBuilder();
    builder.addFieldWithLowestRank("market.displayOrder");
    return builder.build();
  }
}
