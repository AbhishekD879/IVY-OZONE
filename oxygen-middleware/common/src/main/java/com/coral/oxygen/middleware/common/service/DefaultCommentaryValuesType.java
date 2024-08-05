package com.coral.oxygen.middleware.common.service;

public enum DefaultCommentaryValuesType {
  FIRST_PLAYER_ID("1"),
  SECOND_PLAYER_ID("2"),
  AWAY_TEAM_ROLE("Away Team"),
  GENERIC_AWAY_TEAM_ROLE("Generic second player listed"),
  AWAY_TEAM_ROLE_CODE("AWAY"),
  T("T"),
  P("P"),
  HOME_TEAM_ROLE("Home Team"),
  GENERIC_HOME_TEAM_ROLE("Generic first player listed"),
  HOME_TEAM_ROLE_CODE("HOME"),
  IS_ACTIVE_TRUE("true"),
  IS_ACTIVE_FALSE("false"),
  PLAYER_1("PLAYER_1"),
  PLAYER_2("PLAYER_2"),
  FIELD_1("1"),
  FIELD_2("2"),
  SCORE("SCORE");

  private String value;

  DefaultCommentaryValuesType(String value) {
    this.value = value;
  }

  public String getValue() {
    return value;
  }
}
