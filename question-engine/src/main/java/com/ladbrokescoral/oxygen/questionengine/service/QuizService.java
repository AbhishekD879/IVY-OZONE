package com.ladbrokescoral.oxygen.questionengine.service;

import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuizDto;
import java.util.List;
import java.util.Optional;

public interface QuizService {
  List<QuizDto> findLiveQuizzes();

  Optional<QuizDto> findLiveQuiz(String sourceId);

  void findPreviousLiveAndFutureQuizzes();
}
