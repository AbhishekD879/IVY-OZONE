package com.ladbrokescoral.oxygen.bigcompetition.dto.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.group.CompetitionMarketDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.group.GroupModuleDataDto;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class GroupModuleDto extends CompetitionModuleDto {
  private GroupModuleDataDto groupModuleData;
  private List<CompetitionMarketDto> markets = new ArrayList<>();
}
