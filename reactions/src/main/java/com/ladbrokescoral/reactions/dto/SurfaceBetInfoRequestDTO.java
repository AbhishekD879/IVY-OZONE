package com.ladbrokescoral.reactions.dto;

import static com.ladbrokescoral.reactions.util.ValidationHelper.notNull;

/**
 * @author PBalarangakumar 14-06-2023
 */
public record SurfaceBetInfoRequestDTO(String surfaceBetId, String selectionId) {

  public SurfaceBetInfoRequestDTO {
    notNull(surfaceBetId, "surfaceBetId");
    notNull(selectionId, "selectionId");
  }
}
