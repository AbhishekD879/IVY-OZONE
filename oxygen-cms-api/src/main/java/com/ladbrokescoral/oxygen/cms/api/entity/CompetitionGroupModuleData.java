package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
public class CompetitionGroupModuleData {

  @NotNull private Integer sportId;
  @NotNull private Integer areaId;
  private Integer competitionId;
  private List<Integer> competitionIds;
  @NotNull private Integer seasonId;
  @NotNull private Integer numberQualifiers;
  private Map<String, String> details = new HashMap<>();
}
