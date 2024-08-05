package com.ladbrokescoral.oxygen.questionengine.repository;

import com.ladbrokescoral.oxygen.questionengine.model.UserAnswer;

import java.util.List;

public interface CustomUserAnswerRepository {
  List<UserAnswer> findByUsernameSourceIdOrderedByCreatedDateDesc(String usernameSourceId);

  List<UserAnswer> findByQuizIdOrderByCreatedDateDesc(String quizId);
}
