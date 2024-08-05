package com.ladbrokescoral.reactions.client.bpp.dto;

import static com.ladbrokescoral.reactions.util.ValidationHelper.notNull;

/**
 * @author PBalarangakumar 15-06-2023
 */
public record BppTokenRequest(String token) {

  public BppTokenRequest {
    notNull(token, "token");
  }
}
