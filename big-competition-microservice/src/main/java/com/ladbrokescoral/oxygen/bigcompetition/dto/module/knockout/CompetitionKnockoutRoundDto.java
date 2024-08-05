package com.ladbrokescoral.oxygen.bigcompetition.dto.module.knockout;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class CompetitionKnockoutRoundDto {
  private String name;
  private Integer number;
  private boolean active;
  private String abbreviation;
}
