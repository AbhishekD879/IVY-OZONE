package com.ladbrokescoral.oxygen.questionengine.service;

import com.egalacoral.spark.siteserver.model.Event;
import java.util.List;
import java.util.Optional;

public interface SiteServerService {

  Optional<Event> getEventDetails(String eventId);
  List<Integer> findScoresForEvent(Event event);
  boolean isMatchFinished(Event event);

}
