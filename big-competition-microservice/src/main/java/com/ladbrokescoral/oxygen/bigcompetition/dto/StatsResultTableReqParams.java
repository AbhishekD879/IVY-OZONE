package com.ladbrokescoral.oxygen.bigcompetition.dto;

import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class StatsResultTableReqParams {
  private Integer sportId;
  private Integer areaId;
  private Integer competitionId;
  private Integer seasonId;
}
