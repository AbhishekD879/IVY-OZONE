package com.egalacoral.spark.timeform.api.services.endpoints.params;

public class InlineCountParam extends DataParam {

  public static final InlineCountParam ALL_PAGES = new InlineCountParam("allpages");

  public static final InlineCountParam NONE = new InlineCountParam("none");

  public InlineCountParam(String value) {
    super("$inlinecount", new FilterParamValue<String>("%s", value));
  }
}
