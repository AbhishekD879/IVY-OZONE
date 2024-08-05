package com.ladbrokescoral.oxygen.questionengine.model.cms;

import com.fasterxml.jackson.annotation.JsonSetter;
import lombok.Data;

import java.util.Collections;
import java.util.List;

@Data
public class QuizHistory {
  private String sourceId;
  private int previousCount;
  private Quiz live;
  private List<Quiz> previous = Collections.emptyList();

  @JsonSetter
  public QuizHistory setPrevious(List<Quiz> previous) {
    if (previous == null) {
      this.previous = Collections.emptyList();
      return this;
    }
    this.previous = previous;
    return this;
  }
}
