package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Value;

@Value
public class TokenResponse {
  /** Needed to authorize to app */
  private String token;
  /** Needed to regenerate token when it expires */
  private String refreshToken;
}
