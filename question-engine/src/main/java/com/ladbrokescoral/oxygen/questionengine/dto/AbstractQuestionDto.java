package com.ladbrokescoral.oxygen.questionengine.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuestionDetailsDto;
import com.ladbrokescoral.oxygen.questionengine.model.cms.QuestionType;
import lombok.Data;
import lombok.experimental.Accessors;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Stream;

@Data
@Accessors(chain = true)
public abstract class AbstractQuestionDto<S extends AbstractQuestionDto<S, T>, T extends AbstractAnswerDto> {
  private String id;
  private String text;
  private QuestionType questionType;
  private QuestionDetailsDto questionDetails;
  private List<T> answers;
  private Map<String, S> nextQuestions = Collections.emptyMap();

  @JsonIgnore
  public S getNextQuestion(T answer) {
    return nextQuestions.get(answer.getNextQuestionId());
  }

  @SuppressWarnings("unchecked")
  public Stream<S> flatten() {
    return Stream.concat(
        Stream.of((S) this),
        this.getAnswers().stream()
            .map(this::getNextQuestion)
            .filter(Objects::nonNull)
            .distinct()
            .flatMap(AbstractQuestionDto::flatten));
  }
}
