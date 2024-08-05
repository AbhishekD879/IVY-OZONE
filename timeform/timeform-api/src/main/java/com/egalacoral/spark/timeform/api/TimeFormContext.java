package com.egalacoral.spark.timeform.api;

import com.egalacoral.spark.timeform.api.connectivity.RequestPerformer;
import com.egalacoral.spark.timeform.model.internal.TokenData;
import okhttp3.Interceptor;

public class TimeFormContext {

  private final String loginUrl;

  private final String dataUrl;

  private final String imageUrl;

  private final String grUrlSuffix;

  private final String hrUrlSuffix;

  private String userName;

  private TokenData tokenData;

  private RequestPerformer requestPerformer;

  private Interceptor interceptor;

  public TimeFormContext(
      String loginUrl, String dataUrl, String grUrlSuffix, String hrUrlSuffix, String imageUrl) {
    this.loginUrl = loginUrl;
    this.dataUrl = dataUrl;
    this.grUrlSuffix = grUrlSuffix;
    this.hrUrlSuffix = hrUrlSuffix;
    this.imageUrl = imageUrl;
  }

  public String getLoginUrl() {
    return loginUrl;
  }

  public String getDataUrl() {
    return dataUrl;
  }

  public String getGrUrlSuffix() {
    return grUrlSuffix;
  }

  public String getHrUrlSuffix() {
    return hrUrlSuffix;
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

  public Interceptor getInterceptor() {
    return interceptor;
  }

  public void setInterceptor(Interceptor interceptor) {
    this.interceptor = interceptor;
  }

  public String getImageUrl() {
    return imageUrl;
  }
}
