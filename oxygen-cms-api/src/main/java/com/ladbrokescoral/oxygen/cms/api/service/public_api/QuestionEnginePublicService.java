package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.QuestionDto;
import com.ladbrokescoral.oxygen.cms.api.dto.QuizDto;
import com.ladbrokescoral.oxygen.cms.api.dto.QuizHistoryDto;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.EventDetails;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Quiz;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.QuizzesByBrandAndSourceId;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.mapping.QuestionEngineMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.QuestionEngineRepository;
import com.ladbrokescoral.oxygen.cms.api.service.QuestionEngineService;
import java.time.Instant;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.apache.commons.lang3.ObjectUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class QuestionEnginePublicService {

  private static final String URL_SEPARATOR = "/";
  private final QuestionEngineService service;
  private final QuestionEngineRepository repository;
  private final MongoTemplate mongoTemplate;

  public List<QuizDto> getAllQuizzes() {
    return service.findAll().stream()
        .map(QuestionEngineMapper.getInstance()::toDto)
        .collect(Collectors.toList());
  }

  public QuizDto getById(String quizId) {
    return repository
        .findById(quizId)
        .map(QuestionEngineMapper.getInstance()::toDto)
        .orElseThrow(NotFoundException::new);
  }

  public List<QuizDto> getQuizByBrand(String brand) {
    return service.findByBrand(brand).stream()
        .map(QuestionEngineMapper.getInstance()::toDto)
        .collect(Collectors.toList());
  }

  public List<QuizDto> getQuizByBrandAndSourceId(String brand, List<String> sourceId) {
    return service.getQuizzesByBrandAndSourceId(brand, getSourceIdValue(sourceId)).stream()
        .map(QuestionEngineMapper.getInstance()::toDto)
        .collect(Collectors.toList());
  }

  public QuestionDto getQuestion(String quizId, String questionId) {
    return QuestionEngineMapper.getInstance()
        .toQuestionDto(service.getQuestionTree(quizId, questionId));
  }

  /**
   * Return so-called History of the quizzes per brand and sourceId ordered by Start date.
   *
   * <p>History is meant to represent all the quizzes that have already been played as well as
   * so-called Live Quiz which will be on top of the list.
   *
   * <p>Live quizzes is meant to represent quizzes that are being played right now by the customers.
   * Only one such quiz is allowed to exist per brand and sourceId. There might be no Live Quiz
   * present when, well obviously, one is not configured at the moment.
   *
   * @param previousLimit maximum number of items <b>per each</b> QuizHistoryDto <b>excluding</b>
   *     Live Quiz
   */
  public List<QuizHistoryDto> getHistory(String brand, int previousLimit) {
    List<QuizzesByBrandAndSourceId> historyByBrandAndSourceId =
        repository.findHistoryGroupedByBrandAndSourceIdAndActiveIsTrue(
            mongoTemplate, brand, previousLimit + 1);

    if (ObjectUtils.isEmpty(historyByBrandAndSourceId)) {
      return Collections.emptyList();
    }
    return historyByBrandAndSourceId.stream()
        .map(
            history ->
                history.getQuizzes().stream()
                    .map(QuestionEngineMapper.getInstance()::toDto)
                    .collect(Collectors.toList()))
        .filter(ObjectUtils::isNotEmpty)
        .map(history -> toHistoryDto(history, previousLimit))
        .collect(Collectors.toList());
  }

  public QuizHistoryDto getHistory(String brand, List<String> sourceId, int previousLimit) {
    Page<Quiz> quizPage =
        repository
            .findByBrandAndSourceIdAndDisplayFromIsBeforeAndActiveIsTrueOrderByDisplayFromDesc(
                brand,
                getSourceIdValue(sourceId),
                Instant.now(),
                PageRequest.of(0, previousLimit + 1));
    List<QuizDto> quizzesDto =
        quizPage.getContent().stream()
            .map(QuestionEngineMapper.getInstance()::toDto)
            .collect(Collectors.toList());

    if (ObjectUtils.isEmpty(quizzesDto)) {
      throw new NotFoundException();
    }

    return toHistoryDto(quizzesDto, previousLimit);
  }

  public List<QuizDto> getPreviousQuizzesPageByBrandAndSourceId(
      String brand, List<String> sourceId, int pageNumber, int pageSize) {
    Page<Quiz> quizPage =
        repository
            .findByBrandAndSourceIdAndDisplayFromIsBeforeAndDisplayToIsBeforeAndActiveIsTrueOrderByDisplayFromDesc(
                brand,
                getSourceIdValue(sourceId),
                Instant.now(),
                Instant.now(),
                PageRequest.of(pageNumber, pageSize));
    return quizPage.getContent().stream()
        .map(QuestionEngineMapper.getInstance()::toDto)
        .collect(Collectors.toList());
  }

  private QuizHistoryDto toHistoryDto(List<QuizDto> history, int previousLimit) {
    return findLiveQuiz(history)
        .map(liveQuiz -> historyWithLiveQuiz(history, liveQuiz))
        .orElseGet(() -> historyWithoutLiveQuiz(history, previousLimit));
  }

  /**
   * We assume that live quiz must be {@link Quiz#isActive()} and {@link Quiz#getDisplayTo()} is
   * after {@link Instant#now()};
   */
  private Optional<QuizDto> findLiveQuiz(List<QuizDto> history) {
    return history.stream()
        .filter(QuizDto::isActive)
        .filter(quiz -> quiz.getDisplayTo().isAfter(Instant.now()))
        .findFirst();
  }

  private QuizHistoryDto historyWithLiveQuiz(List<QuizDto> history, QuizDto liveQuiz) {
    List<QuizDto> previous = history.subList(1, history.size());

    return new QuizHistoryDto()
        .setLive(liveQuiz)
        .setPrevious(previous)
        .setBrand(liveQuiz.getBrand())
        .setSourceId(liveQuiz.getSourceId())
        .setPreviousCount(previous.size());
  }

  private QuizHistoryDto historyWithoutLiveQuiz(List<QuizDto> history, int previousLimit) {
    List<QuizDto> actualPrevious =
        history.stream()
            .limit(history.size() <= previousLimit ? history.size() : history.size() - 1)
            .collect(Collectors.toList());

    return new QuizHistoryDto()
        .setPrevious(actualPrevious)
        .setBrand(history.get(0).getBrand())
        .setSourceId(history.get(0).getSourceId())
        .setPreviousCount(actualPrevious.size());
  }

  private String getSourceIdValue(List<String> sourceId) {
    return sourceId.stream().collect(Collectors.joining(URL_SEPARATOR, URL_SEPARATOR, ""));
  }

  public void updateQuizWithScores(String quizId, EventDetails eventDetails) {
    Optional<Quiz> maybeQuiz = repository.findById(quizId);
    maybeQuiz.ifPresent(
        quiz -> {
          quiz.setEventDetails(eventDetails);
          service.save(quiz);
        });
  }
}
