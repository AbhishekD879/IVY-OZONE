package com.ladbrokescoral.oxygen.cms.api.service.sporttab;

public enum MainTier2Sports implements AllSports {
  GOLF(18);

  private final int categoryId;

  MainTier2Sports(int categoryId) {
    this.categoryId = categoryId;
  }

  public int getCategoryId() {
    return categoryId;
  }

  @Override
  public String getName() {
    return this.name();
  }
}
