package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class SeasonCacheDto {
  private String id;
  private String seasonName;
  private Instant displayFrom;
  private Instant displayTo;
  private List<TeamCacheDto> teams = new ArrayList<>();
  private List<BadgeTypeCacheDto> badgeTypes = new ArrayList<>();
}
