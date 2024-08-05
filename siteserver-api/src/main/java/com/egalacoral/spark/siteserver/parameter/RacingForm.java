package com.egalacoral.spark.siteserver.parameter;

public enum RacingForm {
  EVENT,
  OUTCOME;

  // TODO: not sure that SiteServer support uppercase. need to check.
  @Override
  public String toString() {
    return this.name().toLowerCase();
  }
}
