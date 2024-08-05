package com.ladbrokescoral.reactions.dto;

import static com.ladbrokescoral.reactions.util.ValidationHelper.notNull;

/**
 * @author PBalarangakumar 22-11-2023
 */
public record AggregateKeys(String deleteKey, String redisValue) {

  public AggregateKeys {
    notNull(deleteKey, "deleteKey");
    notNull(redisValue, "redisValue");
  }
}
