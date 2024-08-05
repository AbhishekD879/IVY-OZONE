package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.ArrayList;
import java.util.List;
import javax.validation.Valid;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CompetitionKnockoutModuleData {

  @Valid List<CompetitionKnockoutRound> rounds = new ArrayList<>();
  @Valid List<CompetitionKnockoutEvent> events = new ArrayList<>();
}
