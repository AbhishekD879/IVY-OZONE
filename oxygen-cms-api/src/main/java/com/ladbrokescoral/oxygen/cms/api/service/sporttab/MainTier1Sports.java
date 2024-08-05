package com.ladbrokescoral.oxygen.cms.api.service.sporttab;

import java.util.Arrays;
import java.util.Set;
import java.util.stream.Collectors;

public enum MainTier1Sports implements AllSports {
  FOOTBALL(16),
  BASKETBALL(6),
  TENNIS(34);

  private final int categoryId;

  MainTier1Sports(int categoryId) {
    this.categoryId = categoryId;
  }

  public int getCategoryId() {
    return categoryId;
  }

  @Override
  public String getName() {
    return this.name();
  }

  public static Set<Integer> categoryIds() {
    return Arrays.stream(values()).map(MainTier1Sports::getCategoryId).collect(Collectors.toSet());
  }
}
