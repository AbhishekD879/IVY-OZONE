package com.ladbrokescoral.oxygen.cms.api.entity.questionengine;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonSetter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;
import java.util.stream.Stream;
import lombok.Data;
import lombok.experimental.Accessors;
import org.apache.commons.lang3.StringUtils;

@Data
@Accessors(chain = true)
public class Question {

  private String id = UUID.randomUUID().toString();
  private List<Answer> answers = new ArrayList<>();
  private Type questionType;
  private String text;
  private String hint;
  private Map<String, Question> nextQuestions = new HashMap<>();
  private QuestionDetails questionDetails = new QuestionDetails();

  @JsonSetter
  public Question setId(String id) {
    if (StringUtils.isNotEmpty(id)) {
      this.id = id;
    }
    return this;
  }

  @JsonIgnore
  public Question getNextQuestion(Answer answer) {
    return nextQuestions.get(answer.getNextQuestionId());
  }

  @JsonIgnore
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
