package com.egalacoral.spark.timeform.api.services.endpoints.params;

public class TopParam extends DataParam {

  private TopParam(int top) {
    super("$top", new SingleParamValue<Integer>(top));
  }

  public static TopParam valueOf(int top) {
    return new TopParam(top);
  }
}
