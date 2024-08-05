package com.ladbrokescoral.oxygen.bigcompetition.dto.statsCenter;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@JsonInclude(JsonInclude.Include.NON_EMPTY)
@Accessors(chain = true)
public class TeamDto {
  private String name; // Russia
  private String obName;
  private String statsCenterName; // Uruguay
  private String abbreviation; // URU
  private String svgId; // c80cecc6-f188-325b-ac3d-b125301a35ff
  private Integer totalPoints; // 3
  private Integer matchesTotal;
  private Integer winTotal;
  private Integer drawTotal;
  private Integer lossTotal;
  private Integer goalDiffTotal;
}
