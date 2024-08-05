package com.ladbrokescoral.oxygen.bigcompetition.dto.module;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class AemModuleDto extends CompetitionModuleDto {
  private String aemPageName;
}
