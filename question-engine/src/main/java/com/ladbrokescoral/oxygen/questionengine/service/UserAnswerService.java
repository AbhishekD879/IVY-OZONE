package com.ladbrokescoral.oxygen.questionengine.service;

import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.QuizSubmitDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.UserAnswerDto;
import com.ladbrokescoral.oxygen.questionengine.model.UserAnswer;

import java.util.List;
import java.util.Optional;

public interface UserAnswerService {
  Optional<UserAnswerDto> findById(UserAnswer.Id id);

  UserAnswerDto getById(UserAnswer.Id id);

  UserAnswerDto save(QuizSubmitDto userAnswer);

  List<UserAnswer> findByQuizIdOrderByCreatedDateDesc(String quizId);

}
