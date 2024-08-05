package com.ladbrokescoral.oxygen.cms.api.service.sporttab;

public enum UntiedSports implements AllSports {
  GREYHOUNDS(19),
  HORSERACING(21);

  private final int categoryId;

  UntiedSports(int categoryId) {
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
