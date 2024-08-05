package com.egalacoral.spark.siteserver.api;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public enum UnaryOperation {
  isTrue("isTrue"),
  isFalse("isFalse"),
  isEmpty("isEmpty"),
  isNotEmpty("isNotEmpty");

  private final String name;

  private UnaryOperation(String s) {
    name = s;
  }

  public boolean equalsName(String otherName) {
    return (otherName == null) ? false : name.equals(otherName);
  }

  public String toString() {
    return this.name;
  }
}
