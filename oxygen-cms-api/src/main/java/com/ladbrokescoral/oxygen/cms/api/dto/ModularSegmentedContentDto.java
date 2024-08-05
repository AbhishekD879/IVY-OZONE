package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class ModularSegmentedContentDto {

  private List<ModuleRibbonTabSegmentedDto> moduleRibbonTabCollection;
  private List<HomeModuleSegmentedDto> homeModuleCollection;
  private boolean displayBuildYourBet;
}
