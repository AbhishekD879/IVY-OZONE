package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Competition;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionTab;
import com.ladbrokescoral.oxygen.cms.api.repository.CompetitionTabRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class CompetitionTabService extends AbstractService<CompetitionTab> {

  private final CompetitionTabRepository competitionTabRepository;
  private final CompetitionSubTabService competitionSubTabService;
  private final CompetitionModuleService competitionModuleService;

  @Autowired
  public CompetitionTabService(
      CompetitionTabRepository competitionTabRepository,
      CompetitionSubTabService competitionSubTabService,
      CompetitionModuleService competitionModuleService) {
    super(competitionTabRepository);
    this.competitionTabRepository = competitionTabRepository;
    this.competitionSubTabService = competitionSubTabService;
    this.competitionModuleService = competitionModuleService;
  }

  /** Is invoked when competition is being created or updated and needs to update all its tabs */
  public void populatePathAndSave(Competition competition, CompetitionTab tab) {
    tab.setPathFromParent(competition);
    populateChildElementsWithPath(tab);
    save(tab);
  }

  /** Is invoked when competitionTab is being created or updated */
  @Override
  public CompetitionTab prepareModelBeforeSave(CompetitionTab tab) {
    populateChildElementsWithPath(tab);
    return tab;
  }

  private void populateChildElementsWithPath(CompetitionTab tab) {
    tab.getCompetitionSubTabs()
        .forEach(subTab -> competitionSubTabService.populatePathAndSave(tab, subTab));
    tab.getCompetitionModules()
        .forEach(module -> competitionModuleService.populatePathAndSave(tab, module));
  }

  @Override
  public List<CompetitionTab> findByBrand(String brand) {
    return competitionTabRepository.findAll();
  }
}
