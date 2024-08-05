package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import lombok.Data;

@Data
public class GameDto {
  private String id;
  private String title;
  private String seasonId;
  private Instant displayFrom;
  private Instant displayTo;
  protected List<GameEventDto> events;
  private Map<Integer, PrizeDto> prizes;
}
