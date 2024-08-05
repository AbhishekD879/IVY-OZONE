package com.ladbrokescoral.oxygen.questionengine.dto.cms;

import com.ladbrokescoral.oxygen.questionengine.dto.AbstractQuizHistoryDto;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents the whole history of the concrete Questing Engine Application.
 */
public class AppQuizHistoryDto extends AbstractQuizHistoryDto<QuizDto, QuizDto> {

  @Override
  public AppQuizHistoryDto withPrevious(List<QuizDto> previous) {
    return (AppQuizHistoryDto) new AppQuizHistoryDto()
        .setLive(getLive())
        .setPreviousCount(getPreviousCount())
        .setSourceId(getSourceId())
        .setPrevious(new ArrayList<>(previous));
  }
}

