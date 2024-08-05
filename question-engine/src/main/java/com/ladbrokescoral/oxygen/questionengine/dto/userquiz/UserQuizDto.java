package com.ladbrokescoral.oxygen.questionengine.dto.userquiz;

import com.ladbrokescoral.oxygen.questionengine.dto.AbstractQuizDto;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;

/**
 * If user has completed the quiz then {@link UserQuizDto#firstQuestion} is populated,
 * {@link UserQuizDto#firstAnsweredQuestion} otherwise.
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Accessors(chain = true)
public class UserQuizDto extends AbstractQuizDto {
  private AnsweredQuestionDto firstAnsweredQuestion;

  @Override
  public AnsweredQuestionDto firstQuestion() {
    return firstAnsweredQuestion;
  }
}
