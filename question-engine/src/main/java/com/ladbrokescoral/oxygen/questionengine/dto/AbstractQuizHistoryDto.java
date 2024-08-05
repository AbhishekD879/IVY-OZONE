package com.ladbrokescoral.oxygen.questionengine.dto;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.With;
import lombok.experimental.Accessors;

import java.util.List;

@Data
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
@Accessors(chain = true)
public abstract class AbstractQuizHistoryDto<L extends AbstractQuizDto, P extends AbstractQuizDto> {

  /**
   * Application identifier.
   */
  private String sourceId;
  private int previousCount;
  private L live;

  @With
  private List<P> previous;
}
