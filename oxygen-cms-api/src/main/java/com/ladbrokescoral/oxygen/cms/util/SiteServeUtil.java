package com.ladbrokescoral.oxygen.cms.util;

import static com.egalacoral.spark.siteserver.api.SiteServerApi.COMPETITION_OUTCOME_NAME_DELIMITERS;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

public class SiteServeUtil {

  private SiteServeUtil() {}

  public static String getHomeTeamFromEventName(String name) {
    return getHomeAwayTeamsFromEventName(name)
        .map(list -> list.get(0)) // home team name is first in event name
        .orElse(null);
  }

  public static String getAwayTeamFromEventName(String name) {
    return getHomeAwayTeamsFromEventName(name)
        .map(list -> list.get(1)) // away team name is second in event name
        .orElse(null);
  }

  public static Optional<List<String>> getHomeAwayTeamsFromEventName(String inputName) {
    return Optional.ofNullable(inputName)
        .map(
            name ->
                Arrays.stream(name.replace("|", "").split(COMPETITION_OUTCOME_NAME_DELIMITERS))
                    .map(String::trim)
                    .collect(Collectors.toList()))
        .filter(names -> names.size() == 2);
  }
}
