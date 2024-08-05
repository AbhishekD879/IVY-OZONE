package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.Competition;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionModule;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionSubTab;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionTab;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionModuleService;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionSubTabService;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionTabService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.CompetitionPublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CompetitionApi implements Public {
  private CompetitionPublicService competitionService;
  private CompetitionTabService competitionTabService;
  private CompetitionSubTabService competitionSubTabService;
  private CompetitionModuleService competitionModuleService;

  @Autowired
  public CompetitionApi(
      CompetitionPublicService competitionService,
      CompetitionTabService competitionTabService,
      CompetitionSubTabService competitionSubTabService,
      CompetitionModuleService competitionModuleService) {
    this.competitionService = competitionService;
    this.competitionTabService = competitionTabService;
    this.competitionSubTabService = competitionSubTabService;
    this.competitionModuleService = competitionModuleService;
  }

  @GetMapping(value = "{brand}/competition")
  public List<Competition> readAll(@PathVariable String brand) {
    return competitionService.readAllByBrand(brand);
  }

  @GetMapping(value = "{brand}/competition/{uri}")
  public Competition findByUri(@PathVariable String brand, @PathVariable String uri) {
    return competitionService.readByBrandAndUri(brand, uri);
  }

  @GetMapping(value = "competition/tab/{id}")
  public CompetitionTab findTabById(@PathVariable String id) {
    return competitionTabService.findOne(id).orElseThrow(NotFoundException::new);
  }

  @GetMapping(value = "competition/subtab/{id}")
  public CompetitionSubTab findSubTabById(@PathVariable String id) {
    return competitionSubTabService.findOne(id).orElseThrow(NotFoundException::new);
  }

  @GetMapping(value = "competition/module/{id}")
  public CompetitionModule findModulebById(@PathVariable String id) {
    return competitionModuleService.findOne(id).orElseThrow(NotFoundException::new);
  }
}
