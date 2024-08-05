package com.ladbrokescoral.oxygen.questionengine.controller.api.v2;

import com.ladbrokescoral.oxygen.questionengine.aspect.annotation.Username;
import com.ladbrokescoral.oxygen.questionengine.model.UserAnswer;
import com.ladbrokescoral.oxygen.questionengine.service.UserAnswerService;
import com.newrelic.api.agent.Trace;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v2/user-answer")
public class UserAnswerControllerV2 {
  private final UserAnswerService userAnswerService;

  @Trace
  @GetMapping("/{username}/{quiz-id}/exists")
  public ResponseEntity<Boolean> findById(@PathVariable @Username String username, @PathVariable("quiz-id") String quizId) {
    return userAnswerService.findById(new UserAnswer.Id(quizId, username))
        .map(userAnswer -> ResponseEntity.ok(true))
        .orElse(ResponseEntity.ok(false));
  }
}
