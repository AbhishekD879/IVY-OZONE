package com.egalacoral.spark.timeform.api.services.endpoints.params;

import java.util.List;
import java.util.stream.IntStream;

public class MultiParamValue<T extends List<Integer>> extends ParamValue {

  private final T value;

  private final String template;

  public MultiParamValue(String template, T value) {
    this.value = value;
    this.template = template;
  }

  @Override
  public String build() {
    int size = value.size();
    StringBuilder templateBuilder = new StringBuilder("(");
    templateBuilder.append(template);
    IntStream.range(0, size - 1)
        .forEach(
            i -> {
              templateBuilder.append(" or ");
              templateBuilder.append(template);
            });
    templateBuilder.append(")");
    return String.format(templateBuilder.toString(), value.toArray());
  }

  public T getValue() {
    return value;
  }
}
