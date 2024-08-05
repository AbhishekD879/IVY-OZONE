package com.ladbrokescoral.oxygen.questionengine.repository.impl;

import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBQueryExpression;
import com.amazonaws.services.dynamodbv2.model.Select;
import com.ladbrokescoral.oxygen.questionengine.model.UserAnswer;
import com.ladbrokescoral.oxygen.questionengine.repository.CustomUserAnswerRepository;
import lombok.RequiredArgsConstructor;
import org.socialsignin.spring.data.dynamodb.core.DynamoDBTemplate;

import java.util.List;

@RequiredArgsConstructor
public class UserAnswerRepositoryImpl implements CustomUserAnswerRepository {
  private static final String USERNAME_SOURCE_ID_GLOBAL_INDEX = "UsernameSourceIdGlobalIndex";
  private static final String CREATED_DATE_LOCAL_INDEX = "CreatedDateLocalIndex";

  private final DynamoDBTemplate dynamoDBTemplate;

  @Override
  public List<UserAnswer> findByUsernameSourceIdOrderedByCreatedDateDesc(String usernameSourceId) {
    return dynamoDBTemplate.query(
        UserAnswer.class,
        new DynamoDBQueryExpression<UserAnswer>()
            .withSelect(Select.ALL_PROJECTED_ATTRIBUTES)
            .withScanIndexForward(false)
            .withConsistentRead(false)
            .withIndexName(USERNAME_SOURCE_ID_GLOBAL_INDEX)
            .withHashKeyValues(new UserAnswer().setUsernameSourceId(usernameSourceId))
    );
  }

  @Override
  public List<UserAnswer> findByQuizIdOrderByCreatedDateDesc(String quizId) {
    return dynamoDBTemplate.query(
        UserAnswer.class,
        new DynamoDBQueryExpression<UserAnswer>()
            .withSelect(Select.ALL_PROJECTED_ATTRIBUTES)
            .withScanIndexForward(false)
            .withConsistentRead(false)
            .withIndexName(CREATED_DATE_LOCAL_INDEX)
            .withHashKeyValues(new UserAnswer().setQuizId(quizId))
    );
  }
}
