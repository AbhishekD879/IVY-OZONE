package com.ladbrokescoral.oxygen.bigcompetition.dto.module.knockout;

import java.util.ArrayList;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CompetitionKnockoutModuleDataDto {
  List<CompetitionKnockoutRoundDto> rounds = new ArrayList<>();
  List<CompetitionKnockoutEventDto> events = new ArrayList<>();
}
