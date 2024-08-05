package com.coral.oxygen.middleware.common.service.featured;

import com.coral.oxygen.middleware.pojos.model.cms.Module;
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContent;
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContentItem;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.EventsModule;
import java.math.BigInteger;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class IdsCollector {
  private Collection<Long> eventsIds;
  private Collection<Long> racingEventsIds;
  private Collection<BigInteger> outcomesIds;
  private Collection<Long> enhMultiplesIds;
  private Collection<Long> outrightEventIds;
  private Collection<String> marketIds;

  public IdsCollector(ModularContent modularContent, ModularContentItem item) {
    Set<Long> eventWitoutOutcomesIds =
        item.getModules().stream()
            .map(Module::getData)
            .flatMap(Collection::stream)
            .filter(eventConfig -> eventConfig.getOutcomeId() == null)
            .filter(eventConfig -> !eventConfig.isOutright())
            .map(EventsModuleData::getId)
            .collect(Collectors.toSet());

    outcomesIds =
        item.getModules().stream()
            .map(Module::getData)
            .flatMap(Collection::stream)
            .filter(eventConfig -> eventConfig.getOutcomeId() != null)
            .filter(eventConfig -> !eventConfig.isOutright())
            .map(EventsModuleData::getOutcomeId)
            .collect(Collectors.toSet());

    Map<String, Long> marketEvents =
        item.getModules().stream()
            .map(Module::getData)
            .flatMap(Collection::stream)
            .filter(eventConfig -> eventConfig.getMarketId() != null)
            .filter(eventConfig -> !eventConfig.isOutright())
            .collect(
                Collectors.toMap(
                    eventConfig -> eventConfig.getMarketId().toString(), EventsModuleData::getId));

    marketIds = marketEvents.keySet();

    outrightEventIds =
        item.getModules().stream()
            .map(Module::getData)
            .flatMap(Collection::stream)
            .filter(EventsModuleData::isOutright)
            .map(EventsModuleData::getId)
            .collect(Collectors.toSet());

    racingEventsIds = new HashSet<>(modularContent.getRacingEventsIds());
    racingEventsIds.retainAll(eventWitoutOutcomesIds);
    enhMultiplesIds = new HashSet<>(modularContent.getEnhMultiplesIds());
    enhMultiplesIds.retainAll(eventWitoutOutcomesIds);
    this.eventsIds = eventWitoutOutcomesIds;
    this.eventsIds.removeAll(enhMultiplesIds);
    this.eventsIds.removeAll(racingEventsIds);
    this.eventsIds.removeAll(marketEvents.values());
  }

  public IdsCollector(ModularContent modularContent, EventsModule item) {
    this(modularContent, item.getData());
  }

  public IdsCollector(ModularContent modularContent, List<EventsModuleData> items) {
    Set<Long> eventWitoutOutcomesIds =
        items.stream()
            .filter(eventConfig -> eventConfig.getOutcomeId() == null)
            .filter(eventConfig -> !eventConfig.isOutright())
            .map(EventsModuleData::getId)
            .collect(Collectors.toSet());

    outcomesIds =
        items.stream()
            .filter(eventConfig -> eventConfig.getOutcomeId() != null)
            .filter(eventConfig -> !eventConfig.isOutright())
            .map(EventsModuleData::getOutcomeId)
            .collect(Collectors.toSet());

    Map<String, Long> marketEvents =
        items.stream()
            .filter(eventConfig -> eventConfig.getMarketId() != null)
            .filter(eventConfig -> !eventConfig.isOutright())
            .collect(
                Collectors.toMap(
                    eventConfig -> eventConfig.getMarketId().toString(), EventsModuleData::getId));

    marketIds = marketEvents.keySet();

    outrightEventIds =
        items.stream()
            .filter(EventsModuleData::isOutright)
            .map(EventsModuleData::getId)
            .collect(Collectors.toSet());

    racingEventsIds = new HashSet<>(modularContent.getRacingEventsIds());
    racingEventsIds.retainAll(eventWitoutOutcomesIds);
    enhMultiplesIds = new HashSet<>(modularContent.getEnhMultiplesIds());
    enhMultiplesIds.retainAll(eventWitoutOutcomesIds);
    this.eventsIds = eventWitoutOutcomesIds;
    this.eventsIds.removeAll(enhMultiplesIds);
    this.eventsIds.removeAll(racingEventsIds);
    this.eventsIds.removeAll(marketEvents.values());
  }

  public IdsCollector(Collection<Long> eventsIds) {
    this.eventsIds = eventsIds;
    this.racingEventsIds = Collections.emptyList();
    this.enhMultiplesIds = Collections.emptyList();
    this.outcomesIds = Collections.emptyList();
    this.outrightEventIds = Collections.emptyList();
    this.marketIds = Collections.emptyList();
  }
}
