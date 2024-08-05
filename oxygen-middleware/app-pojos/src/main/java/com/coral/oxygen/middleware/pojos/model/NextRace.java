package com.coral.oxygen.middleware.pojos.model;

public enum NextRace {
  HR("Horse Racing", "21"),
  GH("Greyhounds", "19");

  private String sportName;

  private String categoryId;

  NextRace(String sportName, String categoryId) {
    this.sportName = sportName;
    this.categoryId = categoryId;
  }

  public String getSportName() {
    return sportName;
  }

  public String getCategoryId() {
    return categoryId;
  }
}
