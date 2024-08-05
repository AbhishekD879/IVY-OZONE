package com.coral.oxygen.middleware.in_play.service;

import com.egalacoral.spark.siteserver.model.Event;
import java.util.List;

public interface OutrightOutcomesFilter {
  List<Event> filterOutcomes(List<Event> events);
}
