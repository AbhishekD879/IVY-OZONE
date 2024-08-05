package com.oxygen.publisher.inplay.context;

import lombok.Getter;

public enum InplaySocketMessages {
  // ---------- in-play v1
  GET_TYPE_REQUEST("GET_TYPE"),
  // IN_PLAY_SPORT_TYPE::categoryId::topLevelType[::marketSelector]::typeId
  GET_TYPE_RESPONSE_TEMPLATE("IN_PLAY_SPORT_TYPE::%s"),
  GET_RIBBON_REQUEST("GET_RIBBON"),
  GET_LS_RIBBON_REQUEST("GET_LS_RIBBON"),
  GET_RIBBON_RESPONSE("INPLAY_SPORTS_RIBBON"),
  GET_LS_RIBBON_RESPONSE("INPLAY_LS_SPORTS_RIBBON"),
  GET_INPLAY_STRUCTURE_REQUEST("GET_INPLAY_STRUCTURE"),
  GET_INPLAY_STRUCTURE_RESPONSE("INPLAY_STRUCTURE"),
  GET_INPLAY_LS_STRUCTURE_REQUEST("GET_INPLAY_LS_STRUCTURE"),
  GET_INPLAY_LS_STRUCTURE_RESPONSE("INPLAY_LS_STRUCTURE"),
  GET_SPORT_REQUEST("GET_SPORT"),
  // IN_PLAY_SPORTS::categoryId::topLevelType
  GET_SPORT_RESPONSE_TEMPLATE("IN_PLAY_SPORTS::%s"),
  IN_PLAY_STRUCTURE_CHANGED("IN_PLAY_STRUCTURE_CHANGED"),
  IN_PLAY_LS_STRUCTURE_CHANGED("IN_PLAY_LS_STRUCTURE_CHANGED"),
  IN_PLAY_SPORT_SEGMENT_CHANGED("IN_PLAY_SPORT_SEGMENT_CHANGED"),
  IN_PLAY_SPORTS_RIBBON_CHANGED("IN_PLAY_SPORTS_RIBBON_CHANGED"),
  IN_PLAY_LS_SPORTS_RIBBON_CHANGED("IN_PLAY_LS_SPORTS_RIBBON_CHANGED"),
  IN_PLAY_SPORT_COMPETITION_CHANGED("IN_PLAY_SPORT_COMPETITION_CHANGED"),
  SUBSCRIBE("subscribe"),
  UNSUBSCRIBE("unsubscribe"),
  APP_VERSION_RESPONSE("version"),
  GET_VIRTUAL_SPORTS_RIBBON_REQUEST("GET_VIRTUAL_SPORTS_RIBBON"),

  GET_VIRTUAL_SPORTS_RIBBON_RESPONSE("GET_VIRTUAL_SPORTS_RIBBON_RESPONSE"),

  VIRTUAL_SPORTS_RIBBON_CHANGED("VIRTUAL_SPORTS_RIBBON_CHANGED");

  @Getter private final String code;

  InplaySocketMessages(final String code) {
    this.code = code;
  }

  public String messageId() {
    return code;
  }
}
