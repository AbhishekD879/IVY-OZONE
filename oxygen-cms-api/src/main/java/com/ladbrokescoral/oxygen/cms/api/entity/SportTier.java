package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.Optional;
import java.util.stream.Stream;

public enum SportTier {
  TIER_1(1),
  TIER_2(2),
  UNTIED(0);

  SportTier(int value) {
    this.value = value;
  }

  public final int value;

  public static Optional<SportTier> from(int value) {
    return Stream.of(SportTier.values()).filter(tier -> tier.value == value).findFirst();
  }
}
