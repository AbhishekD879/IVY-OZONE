package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionSubTab;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionTab;
import com.ladbrokescoral.oxygen.cms.api.repository.CompetitionSubTabRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class CompetitionSubTabService extends AbstractService<CompetitionSubTab> {

  private final CompetitionSubTabRepository competitionSubTabRepository;
  private final CompetitionModuleService competitionModuleService;

  @Autowired
  public CompetitionSubTabService(
      CompetitionSubTabRepository competitionSubTabRepository,
      CompetitionModuleService competitionModuleService) {
    super(competitionSubTabRepository);
    this.competitionSubTabRepository = competitionSubTabRepository;
    this.competitionModuleService = competitionModuleService;
  }

  /**
   * Is invoked when competitionTab is being created or updated and needs to update all its subTabs
   */
  public void populatePathAndSave(
      CompetitionTab parentCompetitionTab, CompetitionSubTab competitionSubTab) {
    competitionSubTab.setPathFromParent(parentCompetitionTab);
    populateChildElementsWithPath(competitionSubTab);
    save(competitionSubTab);
  }

  /** Is invoked when competitionSubTab is being created or updated */
  @Override
  public CompetitionSubTab prepareModelBeforeSave(CompetitionSubTab model) {
    populateChildElementsWithPath(model);
    return model;
  }

  private void populateChildElementsWithPath(CompetitionSubTab subTab) {
    subTab
        .getCompetitionModules()
        .forEach(module -> competitionModuleService.populatePathAndSave(subTab, module));
  }

  @Override
  public List<CompetitionSubTab> findByBrand(String brand) {
    return competitionSubTabRepository.findAll();
  }
}
