package com.ladbrokescoral.oxygen.notification.entities;

public enum MessageType {
  sEVENT("sEVENT"),
  sICENT("sICENT"),
  sSCBRD("sSCBRD"),
  sCLOCK("sCLOCK"),
  GOING_DOWN("going_down"),
  RACE_OFF("race_off"),
  RESULTS("results"),
  NON_RUNNER("non_runner"),
  STREAM_STARTING("stream_starting");

  private String type;

  MessageType(String type) {
    this.type = type;
  }

  public String getType() {
    return type;
  }
}
