package com.ladbrokescoral.oxygen.questionengine.dto;

import com.ladbrokescoral.oxygen.questionengine.model.cms.EndPage;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class AbstractAnswerDto {
  private String id;
  private String text;
  private boolean correctAnswer;
  private String questionAskedId;
  private String nextQuestionId;
  private EndPage endPage;
}
