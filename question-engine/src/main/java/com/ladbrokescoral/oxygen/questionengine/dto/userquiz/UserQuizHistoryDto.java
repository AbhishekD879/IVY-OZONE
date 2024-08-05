package com.ladbrokescoral.oxygen.questionengine.dto.userquiz;

import com.ladbrokescoral.oxygen.questionengine.dto.AbstractQuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.AbstractQuizHistoryDto;

import java.util.ArrayList;
import java.util.List;

/*
 * Represents history of a user within concrete Questing Engine Application.
 */
public class UserQuizHistoryDto extends AbstractQuizHistoryDto<AbstractQuizDto, UserQuizDto> {

  @Override
  public UserQuizHistoryDto withPrevious(List<UserQuizDto> previous) {
    return (UserQuizHistoryDto) new UserQuizHistoryDto()
        .setLive(getLive())
        .setPreviousCount(getPreviousCount())
        .setSourceId(getSourceId())
        .setPrevious(new ArrayList<>(previous));
  }
}
