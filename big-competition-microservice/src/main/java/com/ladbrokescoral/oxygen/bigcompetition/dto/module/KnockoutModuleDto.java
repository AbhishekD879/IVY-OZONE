package com.ladbrokescoral.oxygen.bigcompetition.dto.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.knockout.CompetitionKnockoutEventDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.knockout.CompetitionKnockoutRoundDto;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class KnockoutModuleDto extends CompetitionModuleDto {
  private List<CompetitionKnockoutEventDto> knockoutEvents;
  private List<CompetitionKnockoutRoundDto> knockoutRounds;
}
