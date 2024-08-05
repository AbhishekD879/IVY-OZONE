package com.ladbrokescoral.reactions.dto;

import static com.ladbrokescoral.reactions.util.ValidationHelper.notNull;

/**
 * @author PBalarangakumar 14-06-2023
 */
public record UserReactionDTO(
    String custId, String selectionId, String surfaceBetId, Reaction reactionId) {

  public UserReactionDTO {
    notNull(custId, "custId");
    notNull(selectionId, "selectionId");
    notNull(surfaceBetId, "surfaceBetId");
    notNull(reactionId, "reactionId");
  }
}
