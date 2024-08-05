package com.ladbrokescoral.oxygen.notification.services;

import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.RacingResult;
import java.util.Optional;

public interface SiteServerApiService {

  String CACHE_OUTCOME_NAME = "outcome_name";
  String CACHE_EVENT = "event";
  String CACHE_EVENT_FOR_OUTCOME = "event_for_outcome";
  String CACHE_EVENT_RESULTS = "event_results";

  String getOutcomeName(String outcomeId);

  Optional<Event> getEvent(String eventId);

  Optional<Event> getCachedEvent(String eventId);

  Optional<Event> getCachedEventForOutcome(String selectionId);

  Optional<RacingResult> getCachedRacingResults(String eventId);

  Optional<String> getIGameMediaIdForEvent(String eventId);

  Optional<Event> getCommentaryForEvent(String eventId);
}
