package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class EventDetailsDto {

  private String eventId;
  private String eventName;
  private String startTime;
  private List<Integer> actualScores;
  private boolean liveNow;
}
