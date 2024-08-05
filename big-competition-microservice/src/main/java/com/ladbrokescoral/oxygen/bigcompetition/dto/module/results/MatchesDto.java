package com.ladbrokescoral.oxygen.bigcompetition.dto.module.results;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;

@Data
@EqualsAndHashCode(exclude = {"kickOffTime"})
@Accessors(chain = true)
public class MatchesDto {

  @JsonIgnore private String kickOffTime;
  private Team teamA;
  private Team teamB;
}
