package com.coral.oxygen.middleware.in_play.service.market.selector;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import com.google.gson.Gson;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;
import java.util.List;
import java.util.function.Predicate;
import java.util.stream.Collectors;

/** Created by azayats on 24.05.17. */
public abstract class AbstractMarketSelector implements MarketSelector {

  protected final Gson gson;

  public AbstractMarketSelector(Gson gson) {
    this.gson = gson;
  }

  protected SportSegment getCloneWithFilteredMarkets(SportSegment sportSegment) {
    SportSegment clone = deepClone(sportSegment);
    // remove not acceptable markets
    clone.getEventsByTypeName().stream()
        .map(TypeSegment::getEvents)
        .flatMap(Collection::stream)
        .forEach(event -> event.getMarkets().removeIf(market -> !acceptMarket(market)));
    clone.setMarketSelector(selectorName());

    // remove market without outcomes
    clone.getEventsByTypeName().forEach(AbstractMarketSelector::removeMarketsWithoutOutcomes);
    return clone;
  }

  protected SportSegment updateEventIdsAndCount(SportSegment sportSegment) {
    sportSegment
        .getEventsByTypeName()
        .forEach(
            type -> {
              List<Long> eventsIds =
                  type.getEvents().stream()
                      .map(EventsModuleData::getId)
                      .distinct()
                      .sorted(Comparator.naturalOrder())
                      .collect(Collectors.toList());
              type.setEventsIds(eventsIds);
              type.setEventCount(eventsIds.size());
            });
    ArrayList<Long> eventsIds =
        sportSegment.getEventsByTypeName().stream()
            .map(TypeSegment::getEventsIds)
            .flatMap(Collection::stream)
            .distinct()
            .sorted(Comparator.naturalOrder())
            .collect(Collectors.toCollection(ArrayList::new));
    sportSegment.setEventsIds(eventsIds);
    sportSegment.setEventCount(eventsIds.size());

    return sportSegment;
  }

  @Override
  public List<SportSegment> extract(SportSegment sportSegment) {
    List<SportSegment> result = new ArrayList<>(1);
    SportSegment clone = getCloneWithFilteredMarkets(sportSegment);
    // remove events without markets
    clone
        .getEventsByTypeName()
        .forEach(type -> type.getEvents().removeIf(event -> event.getMarkets().isEmpty()));
    // remove type without events
    clone.getEventsByTypeName().removeIf(type -> type.getEvents().isEmpty());
    boolean atLeastOneMarketIsPresent =
        clone.getEventsByTypeName().stream()
            .map(TypeSegment::getEvents)
            .flatMap(Collection::stream)
            .anyMatch(event -> !event.getMarkets().isEmpty());

    if (atLeastOneMarketIsPresent) {
      result.add(updateEventIdsAndCount(clone));
    }

    return result;
  }

  protected static void removeMarketsWithoutOutcomes(TypeSegment type) {
    Predicate<OutputMarket> marketWithoutOutcome =
        market -> market.getOutcomes() == null || market.getOutcomes().isEmpty();

    type.getEvents().forEach(event -> event.getMarkets().removeIf(marketWithoutOutcome));
  }

  protected SportSegment deepClone(SportSegment sportSegment) {
    return gson.fromJson(gson.toJson(sportSegment), SportSegment.class);
  }

  protected abstract boolean acceptMarket(OutputMarket market);

  protected abstract String selectorName();
}
