package com.egalacoral.spark.timeform.api.services.endpoints.params;

import java.util.Arrays;
import java.util.stream.Collectors;

/** Created by Igor.Domshchikov on 8/8/2016. */
public class ExpandParams extends DataParam {
  public ExpandParams(String... value) {
    super("$expand", new SingleParamValue<>(build(value)));
  }

  private static String build(String... values) {
    return Arrays.asList(values).stream().collect(Collectors.joining(","));
  }
}
