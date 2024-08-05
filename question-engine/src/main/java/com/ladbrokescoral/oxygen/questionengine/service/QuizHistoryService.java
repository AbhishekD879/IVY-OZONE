package com.ladbrokescoral.oxygen.questionengine.service;

import com.ladbrokescoral.oxygen.questionengine.dto.cms.AppQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Quiz;

import java.util.List;

public interface QuizHistoryService {
    AppQuizHistoryDto findQuizHistory(String sourceId);
    List<Quiz> getAllQuizzes();
}
