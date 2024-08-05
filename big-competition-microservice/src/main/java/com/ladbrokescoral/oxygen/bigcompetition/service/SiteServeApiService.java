package com.ladbrokescoral.oxygen.bigcompetition.service;

import com.egalacoral.spark.siteserver.model.Aggregation;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.List;
import java.util.Optional;

public interface SiteServeApiService {

  Optional<Event> getEventWithOutcomesForMarket(String marketId);

  List<Event> getEventWithOutcomesForEventSpecial(List<Integer> eventIds);

  Optional<Event> getEventWithOutcomesForEventKnockout(String eventId);

  List<Event> getEventWithOutcomesForTypeSpecial(List<Integer> typeIds);

  List<Event> getNextEventForType(Integer typeId);

  List<Event> getNextEventForEvent(List<Integer> listOfEventId);

  Optional<List<Aggregation>> getMarketsCountForEvents(List<Integer> listOfEventId);

  Optional<List<Event>> getWholeEventToOutcomeForMarket(String marketIds, boolean showUndisplayed);

  Optional<List<Event>> getEventToOutcomeForMarkets(List<String> marketIds);
}
