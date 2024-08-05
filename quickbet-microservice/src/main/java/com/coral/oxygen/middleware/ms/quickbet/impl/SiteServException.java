package com.coral.oxygen.middleware.ms.quickbet.impl;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;

/**
 * Specific exception that have specific format for UI BMA.
 *
 * <p>Example: 42["31002",{"data":{"error":{"code":"EVENT_NOT_FOUND","description":"Error reading
 * outcome data. Event not found"}}}]
 */
public class SiteServException extends RuntimeException {
  private final transient Messages msg;
  private final transient RegularPlaceBetResponse response;

  public SiteServException(Messages msg, String code, String description) {
    this.msg = msg;
    RegularPlaceBetResponse.Data data = new RegularPlaceBetResponse.Data();
    data.setError(new RegularPlaceBetResponse.Error(code, description));
    this.response = new RegularPlaceBetResponse(data);
  }

  public Messages getMsg() {
    return msg;
  }

  public String getDesc() {
    return this.getResponse().getData().getError().getDescription();
  }

  public RegularPlaceBetResponse getResponse() {
    return response;
  }
}
