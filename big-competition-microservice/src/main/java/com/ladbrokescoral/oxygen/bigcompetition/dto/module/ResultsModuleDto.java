package com.ladbrokescoral.oxygen.bigcompetition.dto.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.results.ResultsModuleDataDto;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class ResultsModuleDto extends CompetitionModuleDto {
  private List<ResultsModuleDataDto> results = new ArrayList<>();
}
