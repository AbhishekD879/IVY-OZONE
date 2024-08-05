package com.egalacoral.spark.timeform.api.services.endpoints.params;

import java.util.List;

public class GreyhoundsIds extends MultiParamValue<List<Integer>> {
  public static final String GREYHOUND_ID_EQ_S = "greyhound_id eq %s";

  public GreyhoundsIds(List<Integer> value) {
    super(GREYHOUND_ID_EQ_S, value);
  }

  @Override
  public String build() {
    return super.build();
  }
}
