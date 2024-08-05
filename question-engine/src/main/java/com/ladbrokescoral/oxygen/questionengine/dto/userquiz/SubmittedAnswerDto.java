package com.ladbrokescoral.oxygen.questionengine.dto.userquiz;

import com.ladbrokescoral.oxygen.questionengine.dto.AbstractAnswerDto;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class SubmittedAnswerDto extends AbstractAnswerDto {
  private boolean isUserChoice;
}
