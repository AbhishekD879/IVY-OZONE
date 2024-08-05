package com.ladbrokescoral.oxygen.questionengine.dto.cms;

import com.ladbrokescoral.oxygen.questionengine.dto.AbstractQuestionDto;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;

@Data
@EqualsAndHashCode(callSuper = true)
@Accessors(chain = true)
public class QuestionDto extends AbstractQuestionDto<QuestionDto, AnswerDto> {

}
