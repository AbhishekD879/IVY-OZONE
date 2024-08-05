package com.ladbrokescoral.oxygen.questionengine.model.cms;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;
import lombok.experimental.Accessors;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Stream;

@Data
@Accessors(chain = true)
public class Question {
  private String id;
  private QuestionType questionType;
  private String text;
  private String hint;
  private Map<String, Question> nextQuestions;
  private List<Answer> answers = new ArrayList<>();
  private QuestionDetails questionDetails;

  @JsonIgnore
  public Question getNextQuestion(Answer answer) {
    return nextQuestions.get(answer.getNextQuestionId());
  }

  public Stream<Question> flatten() {
    return Stream.concat(
        Stream.of(this),
        this.getAnswers().stream()
            .map(this::getNextQuestion)
            .filter(Objects::nonNull)
            .distinct()
            .flatMap(Question::flatten));
  }
}
