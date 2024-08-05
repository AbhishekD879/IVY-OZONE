package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class CreatePotsQuestionDto {
  private Integer questionId;
  private String quesDescription;
  private List<CreatePotsChoiceDto> choices;
}
