package com.ladbrokescoral.oxygen.bigcompetition.dto.module.group;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.bigcompetition.dto.statsCenter.GroupModuleBrGroupDetailDto;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class GroupModuleDataDto {
  private Integer sportId;
  private Integer areaId;
  private Integer competitionId;
  private List<Integer> competitionIds;
  private Integer seasonId;
  private Integer numberQualifiers;

  @JsonProperty("data")
  private List<GroupModuleBrGroupDetailDto> groupModuleBrGroupDetailDtos;

  private Map<String, String> details = new HashMap<>();
}
