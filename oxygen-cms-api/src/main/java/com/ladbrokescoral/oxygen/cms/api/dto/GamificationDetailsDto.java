package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.BadgeType;
import java.util.List;
import lombok.Data;

@Data
public class GamificationDetailsDto extends AbstractEntity {
  private String brand;
  private String seasonId;
  private List<SeasonTeamDto> teams;
  private List<BadgeType> badgeTypes;
}
