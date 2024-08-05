package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.ladbrokescoral.oxygen.questionengine.model.cms.QuizHistory;
import com.ladbrokescoral.oxygen.questionengine.service.AbstractCacheDataSource;
import java.util.Map;
import lombok.AllArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.Cache;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class QuizCacheDataSourceImpl implements AbstractCacheDataSource {

  private static final String QUIZ_HISTORY_MAP = "quizHistoryMap";

  @Value("#{cacheManager.getCache('cmsHistoryQuizzesCache')}")
  private Cache cmsHistoryQuizzesCache;

  @Override
  public void saveQuizHistory(Map<String, QuizHistory> quizHistory) {
    cmsHistoryQuizzesCache.put(QUIZ_HISTORY_MAP, quizHistory);
  }

  @Override
  public Map<String, QuizHistory> getQuizHistory() {
    Map<String, QuizHistory> quizHistoryMapCache =
        cmsHistoryQuizzesCache.get(QUIZ_HISTORY_MAP, Map.class);
    return null != quizHistoryMapCache ? quizHistoryMapCache : null;
  }
}
