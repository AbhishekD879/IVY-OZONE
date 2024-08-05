package com.coral.oxygen.middleware.common.utils;

import com.egalacoral.spark.siteserver.model.Event;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.stream.Collectors;

public class EventLiveStreamMapperUtil {

  private static final Set<String> VALID_DRILLDOWN_TAG_NAMES = new HashSet<>();

  static {
    VALID_DRILLDOWN_TAG_NAMES.add("EVFLAG_RVA");
    VALID_DRILLDOWN_TAG_NAMES.add("EVFLAG_PVM");
    VALID_DRILLDOWN_TAG_NAMES.add("EVFLAG_AVA");
    VALID_DRILLDOWN_TAG_NAMES.add("EVFLAG_IVM");
    VALID_DRILLDOWN_TAG_NAMES.add("EVFLAG_RPM");
    VALID_DRILLDOWN_TAG_NAMES.add("EVFLAG_GVM"); // iGameMedia
  }

  public static boolean isLiveStreamAvailable(Event event) {
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

  private EventLiveStreamMapperUtil() {
    // util
  }
}
