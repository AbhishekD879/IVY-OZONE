package com.ladbrokescoral.oxygen.questionengine.thirdparty.cms;

import com.ladbrokescoral.oxygen.questionengine.model.cms.EventDetails;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Question;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Quiz;
import com.ladbrokescoral.oxygen.questionengine.model.cms.QuizHistory;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;

@FeignClient(name = "cms", url = "${cms.baseUrl}/${application.brand}", decode404 = true)
public interface CmsService {

  @GetMapping("/question-engine/previous/source-id/{sourceId}/{pageNumber}/{pageSize}")
  List<Quiz> findPreviousQuizzes(@PathVariable("sourceId") String sourceId,
                                 @PathVariable(value = "pageNumber") Integer pageNumber,
                                 @PathVariable(value = "pageSize") Integer pageSize);

  @GetMapping("/question-engine/question/{quiz-id}/{question-id}")
  Optional<Question> findQuestion(@PathVariable("quiz-id") String quizId, @PathVariable("question-id") String questionId);

  @GetMapping("/question-engine/history/{previousLimit}")
  List<QuizHistory> findHistory(@PathVariable("previousLimit") int previousLimit);

  @GetMapping("/question-engine/history/source-id/{sourceId}/{previousLimit}")
  Optional<QuizHistory> findHistory(@PathVariable("sourceId") String sourceId, @PathVariable("previousLimit") int previousLimit);

  @GetMapping("/question-engine/{quiz-id}")
  Optional<Quiz> findQuizById(@PathVariable("quiz-id") String quizId);

  default List<Quiz> findLiveQuizzes() {
    return findHistory(0).stream()
        .map(QuizHistory::getLive)
        .filter(Objects::nonNull)
        .collect(Collectors.toList());
  }

  @PutMapping("/question-engine/{quiz-id}/scores")
  void updateQuizEventDetails(@PathVariable("quiz-id") String quizId, @RequestBody EventDetails eventDetails);

  static String normalizeSourceId(String sourceId) {
    return sourceId.replace("/", ",").substring(1);
  }

  @GetMapping("/question-engine/allquizzes")
  List<Quiz> findAllQuizzes();
}
