package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Type;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import lombok.Data;

@Data
public class QuestionDto {

  private String id;
  private List<AnswerDto> answers = new ArrayList<>();
  private Type questionType;
  private String text;
  private String hint;
  private Map<String, QuestionDto> nextQuestions;
  private QuestionDetailsDto questionDetails;
}
