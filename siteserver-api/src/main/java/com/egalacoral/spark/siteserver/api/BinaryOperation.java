package com.egalacoral.spark.siteserver.api;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public enum BinaryOperation {
  equals("equals"),
  notEquals("notEquals"),
  lessThan("lessThan"),
  greaterThan("greaterThan"),
  lessThanOrEqual("lessThanOrEqual"),
  greaterThanOrEqual("greaterThanOrEqual"),
  contains("contains"),
  notContains("notContains"),
  in("in"),
  notIn("notIn"),
  intersects("intersects"),
  notIntersects("notIntersects");

  private final String name;

  private BinaryOperation(String s) {
    name = s;
  }

  public boolean equalsName(String otherName) {
    return (otherName == null) ? false : name.equals(otherName);
  }

  public String toString() {
    return this.name;
  }
}
