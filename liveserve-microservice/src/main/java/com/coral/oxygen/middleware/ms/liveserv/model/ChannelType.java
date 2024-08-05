package com.coral.oxygen.middleware.ms.liveserv.model;

public enum ChannelType {
  sICENT("sICENT"),
  sSCBRD("sSCBRD"),
  sCLOCK("sCLOCK"),
  sEVENT("sEVENT"),
  sEVMKT("sEVMKT"),
  sSELCN("sSELCN"),
  SEVENT("SEVENT"),
  SEVMKT("SEVMKT"),
  SSELCN("SSELCN"),
  sPRICE("sPRICE");

  private String name;

  private ChannelType(String name) {
    this.name = name;
  }

  public String getName() {
    return name;
  }
}
