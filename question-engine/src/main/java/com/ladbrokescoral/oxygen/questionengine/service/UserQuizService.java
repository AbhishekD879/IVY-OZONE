package com.ladbrokescoral.oxygen.questionengine.service;

import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.UserQuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.UserQuizHistoryDto;

import com.ladbrokescoral.oxygen.questionengine.model.Pageable;
import com.ladbrokescoral.oxygen.questionengine.model.UserQuizSearchParams;
import com.ladbrokescoral.oxygen.questionengine.model.UserQuizzesPage;
import java.util.Optional;

public interface UserQuizService {
  UserQuizHistoryDto findUserHistory(UserQuizSearchParams searchParams, int previousLimit);

  Optional<UserQuizDto> findLiveQuiz(UserQuizSearchParams searchParams);

  UserQuizzesPage findPreviousUserQuizzes(UserQuizSearchParams searchParams, Pageable pageable);
}
