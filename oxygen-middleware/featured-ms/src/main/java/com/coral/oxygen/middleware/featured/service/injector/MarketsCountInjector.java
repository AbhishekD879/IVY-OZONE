package com.coral.oxygen.middleware.featured.service.injector;

import static java.util.stream.Collectors.toList;

import com.coral.oxygen.middleware.common.service.featured.IdsCollector;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.api.UnaryOperation;
import com.egalacoral.spark.siteserver.model.Aggregation;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class MarketsCountInjector implements EventsModuleInjector {

  private SiteServerApi siteServerApi;

  @Autowired
  public MarketsCountInjector(SiteServerApi siteServerApi) {
    this.siteServerApi = siteServerApi;
  }

  public void injectData(List<? extends EventsModuleData> items, IdsCollector idsCollector) {
    Collection<Long> eventsIds =
        items.stream()
            .filter(e -> Objects.isNull(e.getOutcomeId()))
            .map(EventsModuleData::getId)
            .collect(Collectors.toSet());
    List<Aggregation> startedMarketsCount = consumeStartedEventsMarketsCount(eventsIds);
    List<Aggregation> notStartedMarketsCount = consumeNotStartedEventsMarketsCount(eventsIds);

    Map<Long, Integer> countsMap =
        notStartedMarketsCount.stream()
            .collect(
                Collectors.toMap(Aggregation::getRefRecordId, Aggregation::getCount, (a, b) -> a));

    countsMap.putAll(
        startedMarketsCount.stream()
            .collect(
                Collectors.toMap(Aggregation::getRefRecordId, Aggregation::getCount, (a, b) -> a)));

    items.stream()
        .filter(d -> d.getId() != null)
        .forEach(
            d -> {
              Integer marketsCount = countsMap.get(d.getId());
              if (marketsCount != null) {
                d.setMarketsCount(marketsCount);
              }
            });
  }

  private List<Aggregation> consumeStartedEventsMarketsCount(Collection<Long> eventsIds) {
    SimpleFilter simpleFilter =
        (SimpleFilter)
            new SimpleFilter.SimpleFilterBuilder()
                .addField("market.isMarketBetInRun")
                .addField("event.isStarted")
                .build();
    Optional<List<Aggregation>> marketsCountForEvent =
        siteServerApi.getMarketsCountForEvent(
            eventsIds.stream().map(Object::toString).collect(toList()), simpleFilter);
    return marketsCountForEvent.isPresent() ? marketsCountForEvent.get() : new ArrayList<>();
  }

  private List<Aggregation> consumeNotStartedEventsMarketsCount(Collection<Long> eventsIds) {
    SimpleFilter simpleFilter =
        (SimpleFilter)
            new SimpleFilter.SimpleFilterBuilder()
                .addUnaryOperation("event.isStarted", UnaryOperation.isFalse)
                .build();
    Optional<List<Aggregation>> marketsCountForEvent =
        siteServerApi.getMarketsCountForEvent(
            eventsIds.stream().map(Object::toString).collect(toList()), simpleFilter);
    return marketsCountForEvent.isPresent() ? marketsCountForEvent.get() : new ArrayList<>();
  }
}
