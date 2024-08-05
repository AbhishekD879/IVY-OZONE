package com.ladbrokescoral.reactions.dto;

import static com.ladbrokescoral.reactions.util.ValidationHelper.notNull;

import java.util.Map;

/**
 * @author PBalarangakumar 14-06-2023
 */
public record UserGlobalCountResponseDTO(
    String custId, Map<String, UserGlobalCountInfo> reactions) {

  public UserGlobalCountResponseDTO {
    notNull(custId, "custId");
  }
}
