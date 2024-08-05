package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.Optional;
import java.util.stream.Stream;

public enum OddsCardHeaderType {
  ONE_TWO_TYPE("oneTwoType"),
  HOME_DRAW_AWAY_TYPE("homeDrawAwayType");

  public final String value;

  OddsCardHeaderType(String value) {
    this.value = value;
  }

  public static Optional<OddsCardHeaderType> from(String value) {
    return Stream.of(OddsCardHeaderType.values())
        .filter(type -> type.value.equals(value))
        .findFirst();
  }
}
