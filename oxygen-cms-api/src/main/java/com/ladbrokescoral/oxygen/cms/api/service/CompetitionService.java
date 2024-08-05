package com.ladbrokescoral.oxygen.cms.api.service;

import com.egalacoral.spark.siteserver.model.Category;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.CompetitionRepository;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.apache.commons.lang3.ObjectUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.util.Assert;

@Component
public class CompetitionService extends AbstractService<Competition> {

  private final CompetitionRepository competitionRepository;
  private final CompetitionTabService competitionTabService;
  private final SiteServeService siteServeService;
  private final SportCategoryService sportCategoryService;

  @Autowired
  public CompetitionService(
      CompetitionRepository competitionRepository,
      CompetitionTabService competitionTabService,
      SiteServeService siteServeService,
      SportCategoryService sportCategoryService) {
    super(competitionRepository);
    this.competitionRepository = competitionRepository;
    this.competitionTabService = competitionTabService;
    this.siteServeService = siteServeService;
    this.sportCategoryService = sportCategoryService;
  }

  @Override
  public List<Competition> findByBrand(String brand) {
    return competitionRepository.findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  public Optional<Competition> getCompetitionByBrandAndUri(String brand, String uri) {
    uri = "/" + uri; // needed as we store uri field in format '/some-uri' in DB.
    return competitionRepository.findByBrandAndUri(brand, uri);
  }

  public Competition getCompetitionByid(String id) {
    Optional<Competition> competition = findOne(id);
    Assert.isTrue(competition.isPresent(), "Competition " + id + " is not found");
    return competition.get();
  }

  public CompetitionTab getCompetitionTab(String compId, String tabId, Competition competition) {
    Optional<CompetitionTab> tab =
        competition.getCompetitionTabs().stream().filter(t -> t.getId().equals(tabId)).findAny();
    Assert.isTrue(tab.isPresent(), "Can't find tab " + tabId + " at competition " + compId);
    return tab.get();
  }

  public CompetitionParticipant getCompetitionParticipant(
      String participantId, Competition competition) {
    Optional<CompetitionParticipant> participant =
        competition.getCompetitionParticipants().stream()
            .filter(p -> p.getId().equals(participantId))
            .findAny();
    return participant.orElseThrow(NotFoundException::new);
  }

  public CompetitionSubTab getCompetitionSubTab(
      String tabId, String subTabId, CompetitionTab competitionTab) {
    Optional<CompetitionSubTab> subTab =
        competitionTab.getCompetitionSubTabs().stream()
            .filter(st -> st.getId().equals(subTabId))
            .findAny();
    Assert.isTrue(subTab.isPresent(), "SubTab" + subTabId + " is not exists at tabId " + tabId);
    return subTab.get();
  }

  public CompetitionModule getCompetitionTabModule(
      String tabId, String moduleId, CompetitionTab tab) {
    Optional<CompetitionModule> module =
        tab.getCompetitionModules().stream().filter(m -> m.getId().equals(moduleId)).findAny();
    Assert.isTrue(module.isPresent(), "Module" + moduleId + " is not exists at tab " + tabId);
    return module.get();
  }

  public CompetitionModule getCompetitionSubTabModule(
      String subTabId, String moduleId, CompetitionSubTab subTab) {
    Optional<CompetitionModule> module =
        subTab.getCompetitionModules().stream().filter(m -> m.getId().equals(moduleId)).findAny();
    Assert.isTrue(module.isPresent(), "Module" + moduleId + " is not exists at subTab " + subTabId);
    return module.get();
  }

  @Override
  public Competition prepareModelBeforeSave(Competition competition) {
    competition.setPath(competition.getUri());
    competition
        .getCompetitionTabs()
        .forEach(tab -> competitionTabService.populatePathAndSave(competition, tab));
    popolateCategoryIdAndClassId(competition);
    return competition;
  }

  private void popolateCategoryIdAndClassId(Competition competition) {
    Optional<List<Category>> classToSubTypeForType =
        siteServeService.getClassToSubTypeForType(
            competition.getBrand(), competition.getTypeId().toString());
    Assert.isTrue(
        classToSubTypeForType.isPresent() && !classToSubTypeForType.get().isEmpty(),
        "Can't find competition at SS by typeId");
    Category clazz = classToSubTypeForType.get().get(0);
    Integer categoryId = clazz.getCategoryId();
    Integer clazzId = clazz.getId();
    Integer typeId = clazz.getTypes().get(0).getId();
    Assert.isTrue(
        competition.getTypeId().equals(typeId),
        "Validation failed! typeIds is different " + competition.getTypeId() + " != " + typeId);
    competition.setCategoryId(categoryId);
    competition.setClazzId(clazzId);
    List<SportCategory> sportCategories =
        Optional.ofNullable(
                sportCategoryService.findSportCategoryByBrandAndImageTitle(
                    competition.getBrand(), competition.getName()))
            .orElse(new ArrayList<>());
    sportCategories.stream()
        .filter(ObjectUtils::isNotEmpty)
        .findAny()
        .ifPresent(sportCategory -> competition.setSportId(sportCategory.getCategoryId()));
  }

  public void updateCompetitionSportId(SportCategory entity) {
    Optional<Competition> competition =
        competitionRepository.findByBrandAndName(entity.getBrand(), entity.getImageTitle());
    if (competition.isPresent()) {
      Competition comp = competition.get();
      comp.setSportId(entity.getCategoryId());
      competitionRepository.save(comp);
    }
  }
}
