package com.ladbrokescoral.oxygen.questionengine.model.cms;

import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class Answer {
  private String id;
  private String text;
  private String questionAskedId;
  private String nextQuestionId;
  private boolean correctAnswer;
  private String selectionId;
  private EndPage endPage;
}
