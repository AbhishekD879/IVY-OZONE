package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class AnswerDto {

  private String id;
  private String text;
  private String questionAskedId;
  private String nextQuestionId;
  private boolean correctAnswer;
  private String selectionId;
  private EndPageDto endPage;
}
