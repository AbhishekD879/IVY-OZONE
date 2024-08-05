package com.ladbrokescoral.oxygen.questionengine.model;

import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBHashKey;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBIndexHashKey;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBIndexRangeKey;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBRangeKey;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBTable;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBTypeConverted;
import com.ladbrokescoral.oxygen.questionengine.dynamodb.converter.InstantConverter;
import com.ladbrokescoral.oxygen.questionengine.dynamodb.converter.QuestionIdToAnswerIdConverter;
import lombok.AccessLevel;
import lombok.Data;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import lombok.experimental.Accessors;

import java.time.Instant;
import java.util.List;
import java.util.Map;

@Data
@DynamoDBTable(tableName = "question-engine-user-answer")
@Accessors(chain = true)
public class UserAnswer {

  @org.springframework.data.annotation.Id
  @Getter(value = AccessLevel.NONE)
  @Setter(value = AccessLevel.NONE)
  private Id id;

  @DynamoDBHashKey
  private String quizId;

  @DynamoDBRangeKey
  private String username;

  @DynamoDBIndexHashKey(attributeName = "usernameSourceId", globalSecondaryIndexName = "UsernameSourceIdGlobalIndex")
  private String usernameSourceId;

  @DynamoDBTypeConverted(converter = QuestionIdToAnswerIdConverter.class)
  private Map<String, List<String>> questionIdToAnswerId;

  @DynamoDBTypeConverted(converter = InstantConverter.class)
  @DynamoDBIndexRangeKey(
      attributeName = "createdDate",
      globalSecondaryIndexName = "UsernameSourceIdGlobalIndex",
      localSecondaryIndexName = "CreatedDateLocalIndex"
  )
  private Instant createdDate;

  @DynamoDBTypeConverted(converter = InstantConverter.class)
  private Instant modifiedDate;


  @Getter
  @ToString
  @RequiredArgsConstructor
  public static class Id {

    @DynamoDBHashKey
    private final String quizId;

    @DynamoDBRangeKey
    private final String username;
  }
}
