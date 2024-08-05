package com.ladbrokescoral.reactions.dto;

import static com.ladbrokescoral.reactions.util.ValidationHelper.notNull;

/**
 * @author PBalarangakumar 12-07-2023
 */
public record GlobalCount(AggregateKeys _id, long count) {

  public GlobalCount {
    notNull(_id, "_id");
    notNull(count, "count");
  }
}
