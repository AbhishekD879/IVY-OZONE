package com.egalacoral.spark.timeform.api;

import com.egalacoral.spark.timeform.api.connectivity.RequestPerformer;
import com.egalacoral.spark.timeform.model.internal.TokenData;

public class TimeFormContext {

  private final String loginUrl;

  private final String dataUrl;

  private String userName;

  private TokenData tokenData;

  private RequestPerformer requestPerformer;

  public TimeFormContext(String loginUrl, String dataUrl) {
    this.loginUrl = loginUrl;
    this.dataUrl = dataUrl;
  }

  public String getLoginUrl() {
    return loginUrl;
  }

  public String getDataUrl() {
    return dataUrl;
  }

  public String getUserName() {
    return userName;
  }

  public void setUserName(String userName) {
    this.userName = userName;
  }

  public TokenData getTokenData() {
    return tokenData;
  }

  public void setTokenData(TokenData tokenData) {
    this.tokenData = tokenData;
  }

  public RequestPerformer getRequestPerformer() {
    return requestPerformer;
  }

  public void setRequestPerformer(RequestPerformer requestPerformer) {
    this.requestPerformer = requestPerformer;
  }
}
