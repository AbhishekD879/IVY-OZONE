package com.ladbrokescoral.oxygen.questionengine.service;

import com.ladbrokescoral.oxygen.questionengine.model.cms.QuizHistory;
import java.util.HashMap;
import java.util.Map;

public interface AbstractCacheDataSource {

  public default Map<String, QuizHistory> getQuizHistory() {
    return new HashMap<>();
  }

  public abstract void saveQuizHistory(Map<String, QuizHistory> t);
}
