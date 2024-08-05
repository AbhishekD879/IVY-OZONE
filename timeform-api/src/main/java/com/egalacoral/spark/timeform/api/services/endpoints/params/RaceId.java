package com.egalacoral.spark.timeform.api.services.endpoints.params;

public class RaceId extends FilterParamValue<Integer> {

  private RaceId(String template, Integer value) {
    super(template, value);
  }

  public static RaceId eq(Integer value) {
    return new RaceId("race_id eq %s", value);
  }

}
