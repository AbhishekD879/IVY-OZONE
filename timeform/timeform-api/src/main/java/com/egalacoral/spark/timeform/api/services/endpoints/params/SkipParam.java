package com.egalacoral.spark.timeform.api.services.endpoints.params;

public class SkipParam extends DataParam {

  private SkipParam(int top) {
    super("$skip", new SingleParamValue<Integer>(top));
  }

  public static SkipParam valueOf(int top) {
    return new SkipParam(top);
  }
}
