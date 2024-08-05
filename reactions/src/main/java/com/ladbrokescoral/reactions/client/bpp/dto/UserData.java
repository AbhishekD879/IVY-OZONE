package com.ladbrokescoral.reactions.client.bpp.dto;

import static com.ladbrokescoral.reactions.util.ValidationHelper.notNull;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * @author PBalarangakumar 15-06-2023
 */
public record UserData(
    String oxiApiToken, @JsonProperty("sportBookUserName") String userName, boolean isUserValid) {

  public UserData {
    notNull(oxiApiToken, "oxiApiToken");
    notNull(userName, "userName");
    notNull(isUserValid, "isUserValid");
  }
}
