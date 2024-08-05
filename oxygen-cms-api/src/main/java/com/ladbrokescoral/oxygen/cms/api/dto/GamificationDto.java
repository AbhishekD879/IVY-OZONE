package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import java.util.List;
import lombok.Data;

@Data
public class GamificationDto {
  private String id;
  private String brand;
  private String seasonId;
  private String seasonName;
  private Instant displayFrom;
  private Instant displayTo;
  private List<SeasonTeamDto> teams;
  private List<BadgeTypeDto> badgeTypes;
}
