package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.Collections;
import java.util.List;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class QuizHistoryDto {
  private String brand;
  private String sourceId;
  private int previousCount;
  private QuizDto live;
  private List<QuizDto> previous = Collections.emptyList();
}
