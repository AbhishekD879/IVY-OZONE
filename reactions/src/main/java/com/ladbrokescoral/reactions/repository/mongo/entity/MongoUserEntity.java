package com.ladbrokescoral.reactions.repository.mongo.entity;

import static com.ladbrokescoral.reactions.util.ValidationHelper.notNull;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * @author PBalarangakumar 17-06-2023
 */
@Document(collection = "users")
public record MongoUserEntity(@Id String redisKey, String redisValue, String deleteKey) {

  public MongoUserEntity {
    notNull(redisKey, "redisKey");
    notNull(redisValue, "redisValue");
    notNull(deleteKey, "deleteKey");
  }
}
