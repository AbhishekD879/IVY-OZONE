package com.ladbrokescoral.oxygen.questionengine.dto.cms;

import java.util.List;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class EventDetailsDto {
  private String eventId;
  private String eventName;
  private String startTime;
  private List<Integer> actualScores;
}
