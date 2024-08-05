package com.ladbrokescoral.oxygen.bigcompetition.dto.module.results;

import java.util.List;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class ResultsModuleDataDto {

  private String date;
  private List<MatchesDto> matches;
}
