package com.ladbrokescoral.oxygen.questionengine.controller.api.v1;

import com.ladbrokescoral.oxygen.questionengine.aspect.annotation.Authenticate;
import com.ladbrokescoral.oxygen.questionengine.aspect.annotation.Username;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.AppQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuestionDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.UserQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.model.Pageable;
import com.ladbrokescoral.oxygen.questionengine.model.UserQuizSearchParams;
import com.ladbrokescoral.oxygen.questionengine.model.UserQuizzesPage;
import com.ladbrokescoral.oxygen.questionengine.service.QuestionService;
import com.ladbrokescoral.oxygen.questionengine.service.QuizHistoryService;
import com.ladbrokescoral.oxygen.questionengine.service.UserQuizService;
import com.newrelic.api.agent.Trace;
import lombok.RequiredArgsConstructor;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.PositiveOrZero;
import java.util.stream.Collectors;

@Validated
@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/quiz")
public class QuizController {
  private final QuizHistoryService quizService;
  private final QuestionService questionService;
  private final UserQuizService userQuizService;

  @GetMapping("/history/")
  @Trace
  public AppQuizHistoryDto findHistory(@RequestParam(value = "source-id") @NotBlank(message = "'source-id' must not be blank") String sourceId,
                                       @RequestParam(value = "previous-limit") @PositiveOrZero @NotNull Integer previousLimit) {
    AppQuizHistoryDto appHistory = quizService.findQuizHistory(sourceId);

    return appHistory.withPrevious(appHistory.getPrevious()
        .stream()
        .limit(previousLimit)
        .collect(Collectors.toList())
    );
  }

  @GetMapping("/history/{username}/")
  @Authenticate
  @Trace
  public UserQuizHistoryDto findHistory(@Username @PathVariable String username,
                                        @RequestParam(value = "source-id") @NotBlank(message = "'source-id' must not be blank") String sourceId,
                                        @RequestParam(value = "previous-limit") @PositiveOrZero @NotNull Integer previousLimit) {
    return userQuizService.findUserHistory(new UserQuizSearchParams(username, sourceId), previousLimit);
  }

  @GetMapping("/previous/{username}/")
  @Authenticate
  @Trace
  public UserQuizzesPage findUserQuizPage(@Username @PathVariable String username,
                                          @RequestParam(value = "source-id") @NotBlank(message = "'source-id' must not be blank") String sourceId,
                                          @RequestParam(value = "page-number") @PositiveOrZero @NotNull Integer pageNumber,@RequestParam(value = "page-size") @PositiveOrZero @NotNull Integer pageSize) {
    return userQuizService.findPreviousUserQuizzes(new UserQuizSearchParams(username, sourceId), new Pageable(pageNumber, pageSize));
  }


  @GetMapping("/question/{quiz-id}/{question-id}")
  @Trace
  public QuestionDto findQuestion(@PathVariable("quiz-id") String quizId, @PathVariable("question-id") String questionId) {
    return questionService.findQuestion(quizId, questionId);
  }
}
