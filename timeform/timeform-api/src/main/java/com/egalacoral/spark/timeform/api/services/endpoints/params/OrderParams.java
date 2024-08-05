package com.egalacoral.spark.timeform.api.services.endpoints.params;

import java.util.Arrays;
import java.util.stream.Collectors;

/** Created by Igor.Domshchikov on 8/17/2016. */
public class OrderParams extends DataParam {

  public OrderParams(String... values) {
    super("$orderby", new SingleParamValue<>(build(values)));
  }

  private static String build(String... values) {
    return Arrays.asList(values).stream().collect(Collectors.joining(","));
  }
}
