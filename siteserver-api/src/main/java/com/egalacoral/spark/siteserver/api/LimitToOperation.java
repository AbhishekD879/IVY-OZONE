package com.egalacoral.spark.siteserver.api;

public enum LimitToOperation {
  HIGHEST("isHighest"),
  LOWEST("isLowest");

  private String name;

  public String getName() {
    return name;
  }

  LimitToOperation(String name) {
    this.name = name;
  }
}
