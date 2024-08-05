package com.egalacoral.spark.timeform.api.services.endpoints.params;

import java.util.Arrays;
import java.util.stream.Collectors;

public class AndParams extends ParamValue {
  ParamValue[] paramValue;

  public AndParams(ParamValue... paramValue) {
    this.paramValue = paramValue;
  }

  @Override
  public String build() {
    return Arrays.stream(paramValue)
        .map(param -> param.build())
        .collect(Collectors.joining(" and "));
  }
}
