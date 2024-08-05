package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.ladbrokescoral.oxygen.questionengine.dto.AbstractQuestionDto;
import com.ladbrokescoral.oxygen.questionengine.dto.AbstractQuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.AppQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.AnsweredQuestionDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.SubmittedAnswerDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.UserQuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.UserQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.model.Pageable;
import com.ladbrokescoral.oxygen.questionengine.model.UserAnswer;
import com.ladbrokescoral.oxygen.questionengine.model.UserQuizSearchParams;
import com.ladbrokescoral.oxygen.questionengine.model.UserQuizzesPage;
import com.ladbrokescoral.oxygen.questionengine.repository.UserAnswerRepository;
import com.ladbrokescoral.oxygen.questionengine.service.QuizHistoryService;
import com.ladbrokescoral.oxygen.questionengine.service.UpsellService;
import com.ladbrokescoral.oxygen.questionengine.service.UserQuizService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Function;
import java.util.stream.Collectors;
@Slf4j
@Service
@RequiredArgsConstructor
public class UserQuizServiceImpl implements UserQuizService {
  private final QuizHistoryService quizService;
  private final UserAnswerRepository userAnswerRepository;
  private final UpsellService upsellService;
  private final ModelMapper modelMapper;

  @Override
  public UserQuizHistoryDto findUserHistory(UserQuizSearchParams searchParams, int previousLimit) {
    AppQuizHistoryDto appHistory = quizService.findQuizHistory(searchParams.getSourceId());
    UserQuizHistoryDto userHistory = modelMapper.map(appHistory, UserQuizHistoryDto.class);

    if (appHistory.getLive() != null) {
      AbstractQuizDto live = this.findUserQuiz(appHistory.getLive(), searchParams.getUsername())
          .map(AbstractQuizDto.class::cast)
          .orElse(appHistory.getLive());

      userHistory.setLive(live);

      upsellService.findUpsellFor(live).ifPresent(live::setUpsell);
    }
    UserQuizzesPage previousUserQuizzesPage = findPreviousUserQuizzes(searchParams, Pageable.firstPage(previousLimit));

    userHistory
        .setPrevious(previousUserQuizzesPage.getQuizzes())
        .setPreviousCount(previousUserQuizzesPage.getTotalRecords());

    return userHistory;
  }

  @Override
  public Optional<UserQuizDto> findLiveQuiz(UserQuizSearchParams searchParams) {
    AppQuizHistoryDto appHistory = quizService.findQuizHistory(searchParams.getSourceId());

    return this.findUserQuiz(appHistory.getLive(), searchParams.getUsername());
  }

  @Override
  public UserQuizzesPage findPreviousUserQuizzes(UserQuizSearchParams searchParams, Pageable pageable) {
    AppQuizHistoryDto history = quizService.findQuizHistory(searchParams.getSourceId());
    QuizDto live = history.getLive();

    Map<String, QuizDto> previousQuizById = history.getPrevious()
        .stream()
        .collect(Collectors.toMap(QuizDto::getId, Function.identity()));
    List<UserAnswer> allAnswers = userAnswerRepository.findByUsernameSourceIdOrderedByCreatedDateDesc(searchParams.getUsername() + searchParams.getSourceId());

    return allAnswers.stream()
        .filter(userAnswer -> previousQuizById.get(userAnswer.getQuizId()) != null)
        .skip(pageable.offset())
        .limit(pageable.limit())
        .map(userAnswer -> modelMapper.map(previousQuizById.get(userAnswer.getQuizId()), UserQuizDto.class)
            .setFirstAnsweredQuestion(toAnsweredQuestion(previousQuizById.get(userAnswer.getQuizId()), userAnswer))
        )
        .collect(Collectors.collectingAndThen(Collectors.toList(), quizzes -> new UserQuizzesPage(previousCount(allAnswers, live), quizzes)));
  }

  private int previousCount(List<UserAnswer> allUserAnswers, QuizDto live) {
    return (live != null && allUserAnswers.stream().anyMatch(userAnswer -> userAnswer.getQuizId().equals(live.getId())))
        ? allUserAnswers.size() - 1
        : allUserAnswers.size();
  }

  private Optional<UserQuizDto> findUserQuiz(QuizDto quiz, String username) {
    return userAnswerRepository.findById(new UserAnswer.Id(quiz.getId(), username))
        .map(userAnswer -> {
          UserQuizDto userQuiz = modelMapper.map(quiz, UserQuizDto.class);

          return userQuiz.setFirstAnsweredQuestion(toAnsweredQuestion(quiz, userAnswer));
        });
  }

  private AnsweredQuestionDto toAnsweredQuestion(QuizDto quiz, UserAnswer userAnswer) {
    AnsweredQuestionDto firstAnsweredQuestion = modelMapper.map(quiz.getFirstQuestion(), AnsweredQuestionDto.class);

    firstAnsweredQuestion.flatten()
        .map(AbstractQuestionDto::getAnswers)
        .flatMap(List::stream)
        .forEach(answerWithResult -> answerWithResult.setUserChoice(isUserChoice(userAnswer, answerWithResult)));

    return firstAnsweredQuestion;
  }

  private boolean isUserChoice(UserAnswer userAnswer, SubmittedAnswerDto answerWithResult) {
    return userAnswer.getQuestionIdToAnswerId()
        .computeIfAbsent(answerWithResult.getQuestionAskedId(), key -> Collections.emptyList())
        .contains(answerWithResult.getId());
  }
}
