package com.egalacoral.spark.liveserver;

public enum ChannelType {
  sICENT("sICENT"),
  sSCBRD("sSCBRD"),
  sCLOCK("sCLOCK"),
  sEVENT("sEVENT"),
  sEVMKT("sEVMKT"),
  sSELCN("sSELCN"),
  SEVENT("SEVENT");

  private String name;

  ChannelType(String name) {
    this.name = name;
  }

  public String getName() {
    return name;
  }
}
