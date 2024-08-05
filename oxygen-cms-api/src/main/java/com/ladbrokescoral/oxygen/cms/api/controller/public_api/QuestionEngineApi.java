package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.QuestionDto;
import com.ladbrokescoral.oxygen.cms.api.dto.QuizDto;
import com.ladbrokescoral.oxygen.cms.api.dto.QuizHistoryDto;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.EventDetails;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.QuestionEnginePublicService;
import java.util.List;
import javax.validation.constraints.PositiveOrZero;
import lombok.RequiredArgsConstructor;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@Validated
@RestController
@RequiredArgsConstructor
public class QuestionEngineApi implements Public {

  private final QuestionEnginePublicService service;
  public static final int DEFAULT_PAGE_NUMBER = 0;
  public static final int DEFAULT_PAGE_SIZE = 3;

  @GetMapping("/{brand}/question-engine")
  public List<QuizDto> getAll(@PathVariable("brand") String brand) {
    return service.getAllQuizzes();
  }

  @GetMapping("/{brand}/question-engine/{quizId}")
  public QuizDto getById(
      @PathVariable("brand") String brand, @PathVariable("quizId") String quizId) {
    return service.getById(quizId);
  }

  @GetMapping("/{brand}/question-engine/source-id/{sourceId}")
  public List<QuizDto> getAllByBrand(
      @PathVariable("brand") String brand, @PathVariable(required = false) List<String> sourceId) {
    return service.getQuizByBrandAndSourceId(brand, sourceId);
  }

  @GetMapping({
    "/{brand}/question-engine/previous/source-id/{sourceId}",
    "/{brand}/question-engine/previous/source-id/{sourceId}/{pageNumber}",
    "/{brand}/question-engine/previous/source-id/{sourceId}/{pageNumber}/{pageSize}",
  })
  public List<QuizDto> getPreviousQuizzesPage(
      @PathVariable("brand") String brand,
      @PathVariable List<String> sourceId,
      @PathVariable(value = "pageNumber", required = false) @PositiveOrZero Integer pageNumber,
      @PathVariable(value = "pageSize", required = false) @PositiveOrZero Integer pageSize) {
    return service.getPreviousQuizzesPageByBrandAndSourceId(
        brand,
        sourceId,
        pageNumber != null ? pageNumber : DEFAULT_PAGE_NUMBER,
        pageSize != null ? pageSize : DEFAULT_PAGE_SIZE);
  }

  @GetMapping("/{brand}/question-engine/question/{quizId}/{questionId}")
  public QuestionDto getQuestionById(
      @PathVariable String brand, @PathVariable String quizId, @PathVariable String questionId) {
    return service.getQuestion(quizId, questionId);
  }

  @GetMapping(
      value = {
        "/{brand}/question-engine/history",
        "/{brand}/question-engine/history/{previousLimit}"
      })
  public List<QuizHistoryDto> getHistory(
      @PathVariable String brand,
      @PathVariable(value = "previousLimit", required = false) @PositiveOrZero
          Integer previousLimit) {
    return service.getHistory(brand, previousLimit != null ? previousLimit : DEFAULT_PAGE_SIZE);
  }

  @GetMapping(
      value = {
        "/{brand}/question-engine/history/source-id/{sourceId}",
        "/{brand}/question-engine/history/source-id/{sourceId}/{previousLimit}"
      })
  public QuizHistoryDto getHistory(
      @PathVariable("brand") String brand,
      @PathVariable("sourceId") List<String> sourceId,
      @PathVariable(value = "previousLimit", required = false) @PositiveOrZero
          Integer previousLimit) {
    return service.getHistory(
        brand, sourceId, previousLimit != null ? previousLimit : DEFAULT_PAGE_SIZE);
  }

  @PutMapping("{brand}/question-engine/{quiz-id}/scores")
  public void updateQuizWithScores(
      @PathVariable("brand") String brand,
      @PathVariable("quiz-id") String quizId,
      @RequestBody EventDetails eventDetails) {
    service.updateQuizWithScores(quizId, eventDetails);
  }

  @GetMapping("/{brand}/question-engine/allquizzes")
  public List<QuizDto> getAllQuizzes(@PathVariable("brand") String brand) {
    return service.getQuizByBrand(brand);
  }
}
