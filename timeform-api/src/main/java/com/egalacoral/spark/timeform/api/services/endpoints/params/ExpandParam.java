package com.egalacoral.spark.timeform.api.services.endpoints.params;

/**
 * Created by Igor.Domshchikov on 8/8/2016.
 */
public class ExpandParam extends DataParam {
  public ExpandParam(String value) {
    super("$expand", new SingleParamValue<>(value));
  }

}
