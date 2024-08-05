package com.ladbrokescoral.cashout.model;

import java.util.Arrays;

public enum ResultCode {
  WIN("Win", "W"),
  LOSE("Lose", "L"),
  HANDICAP("Handicap", "H"),
  PLACE("Place", "P"),
  VOID("Void", "V"),
  UNSET("Unset", "-"),
  UNKNOWN("", "");

  private final String safResultCode;
  private final String accHistoryResultCode;

  public String getSafResultCode() {
    return safResultCode;
  }

  public String getAccHistoryResultCode() {
    return accHistoryResultCode;
  }

  ResultCode(String safResultCode, String accHistoryResultCode) {
    this.safResultCode = safResultCode;
    this.accHistoryResultCode = accHistoryResultCode;
  }

  public static ResultCode fromSAFResultCode(String resultCode) {
    return Arrays.stream(ResultCode.values())
        .filter(e -> e.safResultCode.equalsIgnoreCase(resultCode))
        .findAny()
        .orElse(UNKNOWN);
  }
}
