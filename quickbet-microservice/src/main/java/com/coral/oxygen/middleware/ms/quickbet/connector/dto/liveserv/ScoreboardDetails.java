package com.coral.oxygen.middleware.ms.quickbet.connector.dto.liveserv;

import com.fasterxml.jackson.annotation.JsonProperty;

public class ScoreboardDetails {
  @JsonProperty("value")
  private String value;

  @JsonProperty("role_code")
  private String roleCode;

  public ScoreboardDetails() {}

  public ScoreboardDetails(String roleCode, String value) {
    this.roleCode = roleCode;
    this.value = value;
  }

  public static ScoreboardDetails createHomeEventDetails(String value) {
    return new ScoreboardDetails("HOME", value);
  }

  public static ScoreboardDetails createAwayEventDetails(String value) {
    return new ScoreboardDetails("AWAY", value);
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof ScoreboardDetails)) return false;

    ScoreboardDetails that = (ScoreboardDetails) o;

    if (!value.equals(that.value)) return false;
    return roleCode.equals(that.roleCode);
  }

  @Override
  public int hashCode() {
    int result = value.hashCode();
    result = 31 * result + roleCode.hashCode();
    return result;
  }
}
