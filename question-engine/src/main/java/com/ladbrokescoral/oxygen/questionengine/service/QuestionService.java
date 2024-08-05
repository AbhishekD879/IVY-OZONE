package com.ladbrokescoral.oxygen.questionengine.service;

import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuestionDto;

public interface QuestionService {
  QuestionDto findQuestion(String quizId, String questionId);
}
