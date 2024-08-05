package com.egalacoral.spark.timeform.api.services.endpoints.params;

import java.util.Objects;

public class DataParam {

  private final String name;

  private final ParamValue value;

  public DataParam(String name, ParamValue value) {
    Objects.requireNonNull(name);
    Objects.requireNonNull(value);
    this.name = name;
    this.value = value;
  }

  public String getName() {
    return name;
  }

  public ParamValue getValue() {
    return value;
  }
}
