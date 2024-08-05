package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotEmpty;
import lombok.Data;

@Data
public class EventScore {
  @NotEmpty private String eventId;
  private Integer eventPosition;
  private Integer[] actualScores;
}
