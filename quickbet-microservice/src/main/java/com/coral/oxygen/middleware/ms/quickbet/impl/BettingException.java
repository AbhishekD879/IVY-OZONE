package com.coral.oxygen.middleware.ms.quickbet.impl;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;

public class BettingException extends RuntimeException {
  private final transient Messages msg;
  private final transient RegularPlaceBetResponse response;

  public BettingException(Messages msg, String code, String subCode, String description) {
    this.msg = msg;
    RegularPlaceBetResponse.Data data = new RegularPlaceBetResponse.Data();
    data.setError(new RegularPlaceBetResponse.Error(code, subCode, description));
    this.response = new RegularPlaceBetResponse(data);
  }

  public BettingException(Messages msg, String code, String description) {
    this.msg = msg;
    RegularPlaceBetResponse.Data data = new RegularPlaceBetResponse.Data();
    data.setError(new RegularPlaceBetResponse.Error(code, description));
    this.response = new RegularPlaceBetResponse(data);
  }

  public Messages getMsg() {
    return msg;
  }

  public RegularPlaceBetResponse getResponse() {
    return response;
  }
}
