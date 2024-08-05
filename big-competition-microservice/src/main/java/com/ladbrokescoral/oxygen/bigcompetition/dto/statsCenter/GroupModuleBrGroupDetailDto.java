package com.ladbrokescoral.oxygen.bigcompetition.dto.statsCenter;

import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class GroupModuleBrGroupDetailDto {
  private String competitionId; // 3954
  private String seasonId; // 48238
  private String tableId; // 30334
  private String tableName; // Group A
  private List<TeamDto> teams = new ArrayList<>();
  private List<EventDto> ssEvents;
}
