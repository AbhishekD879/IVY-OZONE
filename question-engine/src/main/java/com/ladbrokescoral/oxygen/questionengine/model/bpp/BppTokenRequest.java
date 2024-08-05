package com.ladbrokescoral.oxygen.questionengine.model.bpp;

import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class BppTokenRequest {
  public static final String TOKEN_PROPERTY_NAME = "token";

  private String token;
}
