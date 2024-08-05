package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.model.output.OutputEvent;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.stream.Collectors;

public class EventLiveStreamAvailableMapper extends ChainedEventMapper {

  private static final Set<String> VALID_DRILLDOWN_TAG_NAMES = new HashSet<>();

  static {
    VALID_DRILLDOWN_TAG_NAMES.add("EVFLAG_RVA");
    VALID_DRILLDOWN_TAG_NAMES.add("EVFLAG_PVM");
    VALID_DRILLDOWN_TAG_NAMES.add("EVFLAG_AVA");
    VALID_DRILLDOWN_TAG_NAMES.add("EVFLAG_IVM");
    VALID_DRILLDOWN_TAG_NAMES.add("EVFLAG_RPM");
  }

  public EventLiveStreamAvailableMapper(EventMapper chain) {
    super(chain);
  }

  @Override
  protected void populate(OutputEvent result, Event event) {
    result.setLiveStreamAvailable(calculateLiveStreamAvailable(event));
  }

  private boolean calculateLiveStreamAvailable(Event event) {
    if (event.getDrilldownTagNames() == null || event.getDrilldownTagNames().trim().isEmpty()) {
      return false;
    }
    String[] split = event.getDrilldownTagNames().split(",");
    int uniqueCount = Arrays.stream(split).map(String::trim).collect(Collectors.toSet()).size();
    if (uniqueCount != split.length) {
      return false;
    }
    return Arrays.stream(split).anyMatch(VALID_DRILLDOWN_TAG_NAMES::contains);
  }
}
