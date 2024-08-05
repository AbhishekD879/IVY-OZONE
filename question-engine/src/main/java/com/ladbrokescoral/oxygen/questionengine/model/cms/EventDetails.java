package com.ladbrokescoral.oxygen.questionengine.model.cms;

import lombok.Data;
import lombok.experimental.Accessors;

import java.util.List;

@Data
@Accessors(chain = true)
public class EventDetails {
  private String eventId;
  private String eventName;
  private String startTime;
  private List<Integer> actualScores;
}
