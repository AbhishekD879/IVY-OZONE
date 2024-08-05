package com.coral.oxygen.middleware.ms.quickbet.utils;

import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.google.common.collect.ImmutableList;
import io.vavr.collection.List;
import java.util.stream.IntStream;

/** Set of methods used for preparing the bets for the testing */
public class BetBuildUtils {

  public static List<Event> outcomeToEvent(String... outcomeIds) {
    return outcomeToEvent(List.of(outcomeIds));
  }

  public static List<Event> outcomeToEvent(List<String> outcomeIds) {
    return outcomeIds.map(BetBuildUtils::event);
  }

  public static List<Event> outcomeToEventWithEventAndMarketId(
      List<String> outcomeIds, List<String> eventIds, List<String> marketIds) {
    return IntStream.range(0, outcomeIds.length())
        .mapToObj(i -> event(outcomeIds.get(i), eventIds.get(i), marketIds.get(i)))
        .collect(List.collector());
  }

  public static Event event(String outcomeId, String eventId, String marketId) {
    Event event = event(outcomeId);
    event.getMarkets().stream().findFirst().ifPresent(market -> market.setId(marketId));
    event.setId(eventId);
    return event;
  }

  public static Event event(String outcomeId) {
    Market market = new Market();

    Event event = new Event();
    Children marketChildren = new Children();
    marketChildren.setMarket(market);
    event.setChildren(ImmutableList.of(marketChildren));

    Children outcomeChildren = new Children();
    outcomeChildren.setOutcome(outcome(outcomeId));
    market.setChildren(ImmutableList.of(outcomeChildren));

    return event;
  }

  public static Outcome outcome(String outcomeId) {
    Outcome outcome = new Outcome();
    outcome.setId(outcomeId);

    return outcome;
  }
}
