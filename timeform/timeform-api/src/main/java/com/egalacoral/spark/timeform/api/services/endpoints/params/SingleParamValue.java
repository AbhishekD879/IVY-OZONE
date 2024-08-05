package com.egalacoral.spark.timeform.api.services.endpoints.params;

public class SingleParamValue<T> extends ParamValue {

  private final T value;

  private final String template;

  public SingleParamValue(T value) {
    this("%s", value);
  }

  public SingleParamValue(String template, T value) {
    this.value = value;
    this.template = template;
  }

  @Override
  public String build() {
    return String.format(template, formatValue());
  }

  protected Object formatValue() {
    return String.valueOf(value);
  }

  public T getValue() {
    return value;
  }
}
