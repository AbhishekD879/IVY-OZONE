package com.ladbrokescoral.oxygen.questionengine.dynamodb.converter;

import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBTypeConverter;

import java.time.Instant;

public class InstantConverter implements DynamoDBTypeConverter<Long, Instant> {

  @Override
  public Long convert(Instant time) {
    return time.toEpochMilli();
  }

  @Override
  public Instant unconvert(Long epoch) {
    return Instant.ofEpochMilli(epoch);
  }
}
