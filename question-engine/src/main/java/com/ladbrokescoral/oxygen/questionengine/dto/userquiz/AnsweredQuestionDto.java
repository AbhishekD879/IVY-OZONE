package com.ladbrokescoral.oxygen.questionengine.dto.userquiz;

import com.ladbrokescoral.oxygen.questionengine.dto.AbstractQuestionDto;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class AnsweredQuestionDto extends AbstractQuestionDto<AnsweredQuestionDto, SubmittedAnswerDto> {

}
