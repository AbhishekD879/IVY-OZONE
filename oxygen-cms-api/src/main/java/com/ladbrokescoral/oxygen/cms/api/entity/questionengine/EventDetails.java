package com.ladbrokescoral.oxygen.cms.api.entity.questionengine;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class EventDetails {

  private String eventId;
  private String eventName;
  private String startTime;
  private List<Integer> actualScores = new ArrayList<>();
  private boolean liveNow;
}
