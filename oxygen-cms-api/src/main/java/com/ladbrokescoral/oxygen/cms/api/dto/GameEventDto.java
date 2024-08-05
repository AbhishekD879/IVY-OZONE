package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import lombok.Data;

@Data
public class GameEventDto {
  private String eventId;
  private Instant startTime;
  private String tvIcon;
  private TeamDto home;
  private TeamDto away;
}
