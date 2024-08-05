package com.egalacoral.spark.timeform.api.services.endpoints.params;

public class FilterParamValue<T> extends SingleParamValue<T> {

  public FilterParamValue(String template, T value) {
    super(template, value);
  }
}
