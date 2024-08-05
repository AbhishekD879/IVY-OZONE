package com.coral.oxygen.middleware.featured.service.injector;

import static java.util.stream.Collectors.toList;

import com.coral.oxygen.middleware.common.mappers.EventMapper;
import com.coral.oxygen.middleware.common.service.ModuleAdapter;
import com.coral.oxygen.middleware.common.service.featured.IdsCollector;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import java.math.BigInteger;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class SingleOutcomeEventsModuleInjector extends ModuleAdapter
    implements EventsModuleInjector {

  private final SiteServerApi siteServerApi;
  private final EventMapper eventMapper;

  @Autowired
  public SingleOutcomeEventsModuleInjector(
      @Qualifier("featured") EventMapper eventMapper, SiteServerApi siteServerApi) {
    this.siteServerApi = siteServerApi;
    this.eventMapper = eventMapper;
  }

  /**
   * this injectData method will call site serve api for fanzone surfacebets to get the data for
   * undisplayed selections
   *
   * @param items event items
   * @param idsCollector selection ids
   * @param includeUndisplayed to include un display selections
   */
  public void injectData(
      List<? extends EventsModuleData> items,
      IdsCollector idsCollector,
      boolean includeUndisplayed) {
    Collection<BigInteger> outcomesIds = idsCollector.getOutcomesIds();

    SimpleFilter simpleFilter =
        (SimpleFilter)
            new SimpleFilter.SimpleFilterBuilder()
                .addBinaryOperation(
                    "event.suspendAtTime", BinaryOperation.greaterThan, Instant.now())
                .build();
    List<String> prune = new ArrayList<>();
    prune.add("event");
    prune.add("market");
    Optional<List<Event>> eventToOutcomeForOutcome =
        siteServerApi.getEventToOutcomeForOutcome(
            outcomesIds.stream()
                .map(String::valueOf)
                .collect(Collectors.toCollection(ArrayList::new)),
            simpleFilter,
            prune,
            includeUndisplayed);
    if (eventToOutcomeForOutcome.isPresent()) {
      Map<String, Event> outcomesMap = generateOutcomesMap(eventToOutcomeForOutcome.get());
      processEventModulesData(items, outcomesMap);
    }
  }
  /**
   * this injectData method will call site serve api for regular surfacebets to get the data for
   * selections as per production
   *
   * @param items event items
   * @param idsCollector selection ids
   */
  public void injectData(List<? extends EventsModuleData> items, IdsCollector idsCollector) {
    Collection<BigInteger> outcomesIds = idsCollector.getOutcomesIds();

    SimpleFilter simpleFilter =
        (SimpleFilter)
            new SimpleFilter.SimpleFilterBuilder()
                .addBinaryOperation(
                    "event.suspendAtTime", BinaryOperation.greaterThan, Instant.now())
                .build();
    List<String> prune = new ArrayList<>();
    prune.add("event");
    prune.add("market");
    Optional<List<Event>> eventToOutcomeForOutcome =
        siteServerApi.getEventToOutcomeForOutcome(
            outcomesIds.stream().map(String::valueOf).collect(toList()), simpleFilter, prune);
    if (eventToOutcomeForOutcome.isPresent()) {
      Map<String, Event> outcomesMap = generateOutcomesMap(eventToOutcomeForOutcome.get());
      processEventModulesData(items, outcomesMap);
    }
  }

  private Map<String, Event> generateOutcomesMap(List<Event> eventsForOutcomes) {
    Map<String, Event> result = new HashMap<>();
    for (Event event : eventsForOutcomes) {
      event
          .getMarkets()
          .forEach(
              market ->
                  market.getOutcomes().forEach(outcome -> result.put(outcome.getId(), event)));
    }
    return result;
  }

  private void processEventModulesData(
      List<? extends EventsModuleData> items, Map<String, Event> outcomesMap) {
    items.stream()
        .filter(d -> d.getOutcomeId() != null) // only items with outcome Ids should be processed
        .filter(d -> outcomesMap.containsKey(String.valueOf(d.getOutcomeId())))
        .forEach(
            d -> {
              eventMapper.map(d, outcomesMap.get(String.valueOf(d.getOutcomeId())));
              d.getMarkets()
                  .forEach(
                      market2 ->
                          market2
                              .getOutcomes()
                              .removeIf(
                                  outcome2 ->
                                      !String.valueOf(d.getOutcomeId()).equals(outcome2.getId())));
              d.getMarkets().removeIf(market2 -> market2.getOutcomes().isEmpty());
            });
  }
}
