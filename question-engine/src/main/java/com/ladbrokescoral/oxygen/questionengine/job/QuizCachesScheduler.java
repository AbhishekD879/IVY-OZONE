package com.ladbrokescoral.oxygen.questionengine.job;

import com.ladbrokescoral.oxygen.questionengine.model.cms.Quiz;
import com.ladbrokescoral.oxygen.questionengine.model.cms.QuizHistory;
import com.ladbrokescoral.oxygen.questionengine.service.AbstractDataSource;
import com.ladbrokescoral.oxygen.questionengine.service.QuizService;
import com.ladbrokescoral.oxygen.questionengine.service.impl.QuizCacheDataSourceImpl;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;

import com.ladbrokescoral.oxygen.questionengine.util.QuizzesUtil;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Service
@Slf4j
@RequiredArgsConstructor
@ConditionalOnProperty("application.cachingEnabled")
public class QuizCachesScheduler {

  private final ModelMapper modelMapper;
  private final QuizService quizService;

  private final List<Quiz> allPriviousQuizes;

  private final Map<String, AbstractDataSource<Quiz>> quizzesMap;

  private final QuizCacheDataSourceImpl quizCacheDataSource;

  @Scheduled(fixedDelayString = "${application.quizSchedulerPeriod}")
  public void saveQuizCaches() {
    if (quizzesMap.size() > 0 || !allPriviousQuizes.isEmpty()) {
      saveQuizzesCache();
    } else {
      quizService.findPreviousLiveAndFutureQuizzes();
    }
  }

  private void saveQuizzesCache() {
    log.debug("Start : saveQuizzesCache :: " + quizzesMap.size());
    Map<String, QuizHistory> quizHistoryMap = new HashMap<>();
    List<Quiz> liveQuizzes = new ArrayList<>();
    prevAndLiveQuizzes(liveQuizzes);
    getQuizHistoryMap(quizHistoryMap, liveQuizzes);
    quizCacheDataSource.saveQuizHistory(quizHistoryMap);
  }

  private void getQuizHistoryMap(Map<String, QuizHistory> quizHistoryMap, List<Quiz> liveQuizzes) {
    Map<String, List<Quiz>> previousQuizzesMap =
        allPriviousQuizes.stream()
            .filter(Quiz::isActive)
            .collect(Collectors.groupingBy(Quiz::getSourceId));
    if (!CollectionUtils.isEmpty(previousQuizzesMap)) {
      previousQuizzesMap.forEach(
          (String sourceId, List<Quiz> quizList) -> {
            QuizHistory quizHistory = new QuizHistory();
            quizHistory.setSourceId(sourceId);
            quizHistory.setPrevious(quizList);
            if (!liveQuizzes.isEmpty()) {
              Quiz quiz = liveQuizzes.get(0);
              if (null != quiz && quiz.getSourceId().equals(sourceId)) {
                quizHistory.setLive(quiz);
              }
            }
            quizHistoryMap.put(sourceId, quizHistory);
          });
    }
  }

  private void prevAndLiveQuizzes(List<Quiz> liveQuizzes) {
    if (!CollectionUtils.isEmpty(quizzesMap)) {
      quizzesMap.forEach(
          (String sourceId, AbstractDataSource<Quiz> quizData) -> {
            AbstractDataSource<Quiz> priorityQueueQuiz = quizData;
            Quiz quiz = priorityQueueQuiz.getPeek();
            if (null != quiz && quiz.getDisplayTo().isBefore(Instant.now())) {
              allPriviousQuizes.add(priorityQueueQuiz.getPoll());
            } else {
              if (QuizzesUtil.isLiveQuiz(quiz)) {
                liveQuizzes.add(priorityQueueQuiz.getPeek());
              }
            }
          });
    }
  }
}
