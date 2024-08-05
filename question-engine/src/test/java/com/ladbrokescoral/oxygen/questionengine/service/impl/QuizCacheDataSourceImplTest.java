package com.ladbrokescoral.oxygen.questionengine.service.impl;

import static org.junit.Assert.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.questionengine.model.cms.QuizHistory;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.cache.Cache;
import org.springframework.cache.support.SimpleValueWrapper;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(MockitoJUnitRunner.class)
public class QuizCacheDataSourceImplTest {

  @Mock private Cache cache;

  @InjectMocks private QuizCacheDataSourceImpl quizCacheDataSource;

  private QuizHistory quizHistory = null;

  @Before
  public void setUp() throws IOException {
    quizHistory = new QuizHistory();
    quizHistory.setSourceId("/quiz");

    ReflectionTestUtils.setField(quizCacheDataSource, "cmsHistoryQuizzesCache", cache);
  }

  @Test
  public void tstQuizCacheDataSource() {
    Map<String, QuizHistory> quizHistoryMap = new HashMap<>();
    quizHistoryMap.put("/quiz", quizHistory);

    quizCacheDataSource.saveQuizHistory(quizHistoryMap);
    when(cache.get("quizHistoryMap",Map.class)).thenReturn(quizHistoryMap);
    assertEquals(quizCacheDataSource.getQuizHistory(), quizHistoryMap);
  }
}
