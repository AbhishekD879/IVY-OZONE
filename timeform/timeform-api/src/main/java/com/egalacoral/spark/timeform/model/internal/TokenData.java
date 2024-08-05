package com.egalacoral.spark.timeform.model.internal;

import com.google.gson.annotations.SerializedName;

public class TokenData {

  @SerializedName("access_token")
  private String accessToken;

  @SerializedName("token_type")
  private String tokenType;

  @SerializedName("expires_in")
  private Integer expiresIn;

  @SerializedName("userName")
  private String userName;

  @SerializedName(".issued")
  private String issuedInfo;

  @SerializedName(".expires")
  private String expiresInfo;

  public String getAccessToken() {
    return accessToken;
  }

  public void setAccessToken(String accessToken) {
    this.accessToken = accessToken;
  }

  public String getTokenType() {
    return tokenType;
  }

  public Integer getExpiresIn() {
    return expiresIn;
  }

  public String getUserName() {
    return userName;
  }

  public String getIssuedInfo() {
    return issuedInfo;
  }

  public String getExpiresInfo() {
    return expiresInfo;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("TokenData{");
    sb.append("accessToken='")
        .append(accessToken == null ? null : accessToken.substring(0, 6))
        .append("...'");
    sb.append(", tokenType='").append(tokenType).append('\'');
    sb.append(", expiresIn=").append(expiresIn);
    sb.append(", userName='").append(userName).append('\'');
    sb.append(", issuedInfo='").append(issuedInfo).append('\'');
    sb.append(", expiresInfo='").append(expiresInfo).append('\'');
    sb.append('}');
    return sb.toString();
  }
}
