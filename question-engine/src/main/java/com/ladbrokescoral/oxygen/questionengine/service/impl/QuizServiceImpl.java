package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuizDto;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Quiz;
import com.ladbrokescoral.oxygen.questionengine.service.AbstractDataSource;
import com.ladbrokescoral.oxygen.questionengine.service.QuizHistoryService;
import com.ladbrokescoral.oxygen.questionengine.service.QuizService;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.cms.CmsService;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

import com.ladbrokescoral.oxygen.questionengine.util.QuizzesUtil;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Service
@RequiredArgsConstructor
@Slf4j
public class QuizServiceImpl implements QuizService {
  private final CmsService cmsService;
  private final QuizHistoryService quizHistoryService;
  private final ModelMapper modelMapper;

  private final List<Quiz> allPriviousQuizes;

  private final Map<String, AbstractDataSource<Quiz>> quizzesMap;

  @Override
  @Cacheable(cacheNames = "liveQuizCache", key = "'$LIVE_QUIZZES'")
  public List<QuizDto> findLiveQuizzes() {
    return cmsService.findLiveQuizzes().stream()
        .map(quiz -> modelMapper.map(quiz, QuizDto.class))
        .collect(Collectors.toList());
  }

  @Override
  public Optional<QuizDto> findLiveQuiz(String sourceId) {
    return Optional.ofNullable(quizHistoryService.findQuizHistory(sourceId).getLive());
  }

  @Override
  public void findPreviousLiveAndFutureQuizzes() {
    List<Quiz> quizzes = quizHistoryService.getAllQuizzes();

    if(quizzes != null) {
      List<Quiz> previousQuizzes =
              quizzes.stream()
                      .filter(Quiz::isActive)
                      .filter(quiz -> quiz.getDisplayTo().isBefore(Instant.now()))
                      .collect(Collectors.toList());

      if (!previousQuizzes.isEmpty()) {
        allPriviousQuizes.clear();
        allPriviousQuizes.addAll(previousQuizzes);
      }

      Map<String, List<Quiz>> liveAndFutureQuizzes =
              quizzes.stream()
                      .filter(Quiz::isActive)
                      .filter(QuizzesUtil::isLiveAndFutureQuizzes)
                      .collect(Collectors.groupingBy(Quiz::getSourceId));

      if (!CollectionUtils.isEmpty(liveAndFutureQuizzes)) {
        liveAndFutureQuizzes.forEach(
                (String sourceId, List<Quiz> quizList) -> {
                  QuizDataSourceImpl quizDataSource = new QuizDataSourceImpl();
                  quizDataSource.addAll(quizList);
                  quizzesMap.put(sourceId, quizDataSource);
                });
      }

      log.info("quizzes size: {}, previousQuizzes size: {}, quizzesMap size: {}", quizzes.size(),allPriviousQuizes.size(),quizzesMap.size());
    }

  }

}
