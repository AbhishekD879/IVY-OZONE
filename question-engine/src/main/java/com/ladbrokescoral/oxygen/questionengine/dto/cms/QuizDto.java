package com.ladbrokescoral.oxygen.questionengine.dto.cms;

import com.ladbrokescoral.oxygen.questionengine.dto.AbstractQuizDto;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.lang3.StringUtils;

@Data
@EqualsAndHashCode(callSuper = true)
@Accessors(chain = true)
public class QuizDto extends AbstractQuizDto {
  private QuestionDto firstQuestion;

  @Override
  public QuestionDto firstQuestion() {
    return firstQuestion;
  }

  public boolean isEventScoresEmpty() {
    EventDetailsDto details = this.getEventDetails();
    return details == null ||
        CollectionUtils.isEmpty(details.getActualScores()) ||
        details.getActualScores().size() < 2 ||
        isActualScoresValuesNull(details);
  }

  private boolean isActualScoresValuesNull(EventDetailsDto eventDetails) {
    return eventDetails.getActualScores().size() == 2 &&
        eventDetails.getActualScores().get(0) == null &&
        eventDetails.getActualScores().get(1) == null;
  }

  public boolean isEventStartTimeEmpty() {
    return this.getEventDetails() != null && StringUtils.isEmpty(this.getEventDetails().getStartTime());
  }
}
