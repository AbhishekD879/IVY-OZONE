package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class GamificationDetailsPublicDto {
  private String id;
  private String brand;
  private String seasonId;
  private String seasonName;
  private List<SeasonTeamPublicDto> teams;
  private List<BadgeTypeDto> badgeTypes;
}
