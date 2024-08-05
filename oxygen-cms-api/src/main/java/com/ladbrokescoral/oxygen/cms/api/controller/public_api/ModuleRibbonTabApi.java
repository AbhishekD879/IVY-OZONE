package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.ModuleRibbonTabDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ModuleRibbonTabPublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ModuleRibbonTabApi implements Public {

  private final ModuleRibbonTabPublicService moduleRibbonTabService;

  @Autowired
  public ModuleRibbonTabApi(ModuleRibbonTabPublicService moduleRibbonTabService) {
    this.moduleRibbonTabService = moduleRibbonTabService;
  }

  @GetMapping(value = "module-ribbon-tabs")
  public List<ModuleRibbonTabDto> findAll() {

    return moduleRibbonTabService.findAll();
  }
}
