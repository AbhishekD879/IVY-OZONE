package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.ModuleRibbonTabDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ModuleRibbonTab;
import com.ladbrokescoral.oxygen.cms.api.mapping.ModuleRibbonTabMapper;
import com.ladbrokescoral.oxygen.cms.api.service.BybTabAvailabilityService;
import com.ladbrokescoral.oxygen.cms.api.service.ModuleRibbonTabService;
import java.util.ArrayList;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ModuleRibbonTabPublicService {
  public static final String BUILD_YOUR_BET_TAB = "tab-build-your-bet";

  private final ModuleRibbonTabService moduleRibbonTabService;
  private final BybTabAvailabilityService bybTabAvailabilityService;

  public List<ModuleRibbonTabDto> findAll() {
    List<ModuleRibbonTab> allRibbonTabs = moduleRibbonTabService.findAllUniversalModuleRibbonTabs();

    List<ModuleRibbonTabDto> result = new ArrayList<>();
    for (ModuleRibbonTab moduleRibbonTab : allRibbonTabs) {
      if (BUILD_YOUR_BET_TAB.equals(moduleRibbonTab.getInternalId())
          && !bybTabAvailabilityService.isBybEnabledAndLeaguesAvailable("bma")) {
        continue;
      }

      result.add(ModuleRibbonTabMapper.INSTANCE.toDto(moduleRibbonTab));
    }
    return result;
  }
}
