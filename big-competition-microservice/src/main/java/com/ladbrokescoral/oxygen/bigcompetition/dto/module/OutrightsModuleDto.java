package com.ladbrokescoral.oxygen.bigcompetition.dto.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.group.CompetitionMarketDto;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class OutrightsModuleDto extends CompetitionModuleDto {
  private List<CompetitionMarketDto> markets = new ArrayList<>();
}
