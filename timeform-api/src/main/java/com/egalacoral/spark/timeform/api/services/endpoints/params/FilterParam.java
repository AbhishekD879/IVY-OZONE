package com.egalacoral.spark.timeform.api.services.endpoints.params;

public class FilterParam extends DataParam {

  public static FilterParam create(ParamValue value) {
    return new FilterParam(value);
  }

  private FilterParam(ParamValue value) {
    super("$filter", value);
  }

}
