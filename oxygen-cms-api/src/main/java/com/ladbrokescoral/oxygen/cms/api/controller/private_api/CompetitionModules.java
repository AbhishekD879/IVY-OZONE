package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Competition;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionModule;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionSubTab;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionTab;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionModuleService;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionService;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionSubTabService;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionTabService;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import javax.validation.constraints.NotEmpty;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.Assert;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CompetitionModules extends AbstractCrudController<CompetitionModule> {
  private CompetitionService competitionService;
  private CompetitionTabService competitionTabService;
  private CompetitionSubTabService competitionSubTabService;
  private CompetitionModuleService competitionModuleService;

  @Autowired
  CompetitionModules(
      CompetitionSubTabService competitionSubTabService,
      CompetitionService competitionService,
      CompetitionTabService competitionTabService,
      CompetitionModuleService competitionModuleService) {
    super(competitionModuleService);
    this.competitionService = competitionService;
    this.competitionTabService = competitionTabService;
    this.competitionSubTabService = competitionSubTabService;
    this.competitionModuleService = competitionModuleService;
  }

  @PostMapping("competition/{compId}/tab/{tabId}/subTab/{subTabId}/module")
  public ResponseEntity createSubTabModule(
      @RequestBody @Validated CompetitionModule entity,
      @PathVariable @NotEmpty String compId,
      @PathVariable @NotEmpty String tabId,
      @PathVariable @NotEmpty String subTabId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    CompetitionTab tab = competitionService.getCompetitionTab(compId, tabId, competition);
    CompetitionSubTab subTab = competitionService.getCompetitionSubTab(tabId, subTabId, tab);
    entity.setPathFromParentCompetitionSubTab(subTab);
    competitionModuleService.updateMaxDisplayValue(entity);
    CompetitionModule module = super.createEntity(entity);
    Assert.isTrue(null != module, "Module is not created");
    List<CompetitionModule> modules =
        Optional.ofNullable(subTab.getCompetitionModules()).orElse(new ArrayList<>());
    modules.add(module);
    subTab.setCompetitionModules(modules);
    competitionModuleService.validateCompetitionId(entity);
    competitionModuleService.populateCompetitionIdsForGroupWidgetModule(entity, competition);
    competitionSubTabService.save(subTab);
    return new ResponseEntity<>(module, HttpStatus.CREATED);
  }

  @PostMapping("competition/{compId}/tab/{tabId}/module")
  public ResponseEntity createTabModule(
      @RequestBody @Validated CompetitionModule entity,
      @PathVariable @NotEmpty String compId,
      @PathVariable @NotEmpty String tabId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    CompetitionTab tab = competitionService.getCompetitionTab(compId, tabId, competition);
    entity.setPathFromParentCompetitionTab(tab);
    competitionModuleService.updateMaxDisplayValue(entity);
    CompetitionModule module = super.createEntity(entity);
    Assert.isTrue(null != module, "Module is not created");
    List<CompetitionModule> modules =
        Optional.ofNullable(tab.getCompetitionModules()).orElse(new ArrayList<>());
    modules.add(module);
    tab.setCompetitionModules(modules);
    competitionModuleService.validateCompetitionId(entity);
    competitionModuleService.populateCompetitionIdsForGroupWidgetModule(entity, competition);
    competitionTabService.save(tab);
    return new ResponseEntity<>(module, HttpStatus.CREATED);
  }

  @GetMapping("competition/{compId}/tab/{tabId}/module/{moduleId}")
  public ResponseEntity readCompetitionTabModule(
      @PathVariable @NotEmpty String compId,
      @PathVariable @NotEmpty String tabId,
      @PathVariable @NotEmpty String moduleId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    CompetitionTab tab = competitionService.getCompetitionTab(compId, tabId, competition);
    CompetitionModule module = competitionService.getCompetitionTabModule(tabId, moduleId, tab);
    populateCreatorAndUpdater(competition);
    populateCreatorAndUpdater(tab);
    populateCreatorAndUpdater(module);
    competition.setCompetitionTabs(Arrays.asList(tab));
    tab.setCompetitionModules(Arrays.asList(module));
    return new ResponseEntity<>(competition, HttpStatus.OK);
  }

  @GetMapping("competition/{compId}/tab/{tabId}/subTab/{subTabId}/module/{moduleId}")
  public ResponseEntity readCompetitionTabSubTabModule(
      @PathVariable @NotEmpty String compId,
      @PathVariable @NotEmpty String tabId,
      @PathVariable @NotEmpty String subTabId,
      @PathVariable @NotEmpty String moduleId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    CompetitionTab tab = competitionService.getCompetitionTab(compId, tabId, competition);
    CompetitionSubTab subTab = competitionService.getCompetitionSubTab(tabId, subTabId, tab);
    CompetitionModule module =
        competitionService.getCompetitionSubTabModule(subTabId, moduleId, subTab);
    populateCreatorAndUpdater(competition);
    populateCreatorAndUpdater(tab);
    populateCreatorAndUpdater(subTab);
    populateCreatorAndUpdater(module);
    competition.setCompetitionTabs(Arrays.asList(tab));
    tab.setCompetitionSubTabs(Arrays.asList(subTab));
    subTab.setCompetitionModules(Arrays.asList(module));
    return new ResponseEntity<>(competition, HttpStatus.OK);
  }

  @GetMapping("competitionModule")
  @Override
  public List<CompetitionModule> readAll() {
    return super.readAll();
  }

  @GetMapping("competitionModule/{id}")
  @Override
  public CompetitionModule read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping("competitionModule/{id}")
  @Override
  public CompetitionModule update(
      @PathVariable String id, @RequestBody @Validated CompetitionModule updateEntity) {
    CompetitionModule existingModule =
        competitionModuleService.findOne(id).orElseThrow(NotFoundException::new);
    updateEntity.setPath(existingModule.getPath());
    competitionModuleService.validateCompetitionId(updateEntity);
    competitionModuleService.populateCompetitionIdsForGroupWidgetModule(updateEntity);
    competitionModuleService.updateMaxDisplayValue(updateEntity);
    return super.update(id, updateEntity);
  }

  @PostMapping("competition/{compId}/tab/{tabId}/module/ordering")
  public ResponseEntity orderSubTabModules(
      @RequestBody OrderDto newOrder,
      @PathVariable @NotEmpty String compId,
      @PathVariable @NotEmpty String tabId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    CompetitionTab tab = competitionService.getCompetitionTab(compId, tabId, competition);
    int sortedIdSize = newOrder.getOrder().size();
    int dbItemSize = tab.getCompetitionModules().size();
    validateSortedItemsSize(sortedIdSize, dbItemSize);
    List<CompetitionModule> sortedCollection =
        newOrder.getOrder().stream()
            .map(item -> super.crudService.findOne(item).get())
            .collect(Collectors.toList());
    tab.setCompetitionModules(sortedCollection);
    competitionTabService.save(tab);
    return new ResponseEntity(HttpStatus.OK);
  }

  @PostMapping("competition/{compId}/tab/{tabId}/subTab/{subTabId}/module/ordering")
  public ResponseEntity orderSubTabModules(
      @RequestBody OrderDto newOrder,
      @PathVariable @NotEmpty String compId,
      @PathVariable @NotEmpty String tabId,
      @PathVariable @NotEmpty String subTabId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    CompetitionTab tab = competitionService.getCompetitionTab(compId, tabId, competition);
    CompetitionSubTab subTab = competitionService.getCompetitionSubTab(tabId, subTabId, tab);
    int sortedIdSize = newOrder.getOrder().size();
    int dbItemSize = subTab.getCompetitionModules().size();
    validateSortedItemsSize(sortedIdSize, dbItemSize);
    List<CompetitionModule> sortedCollection =
        newOrder.getOrder().stream()
            .map(item -> super.crudService.findOne(item).get())
            .collect(Collectors.toList());
    subTab.setCompetitionModules(sortedCollection);
    competitionSubTabService.save(subTab);
    return new ResponseEntity(HttpStatus.OK);
  }

  @PutMapping("competitionModule/{id}/{brand}")
  public CompetitionModule updateByBrand(
      @PathVariable String id,
      @PathVariable String brand,
      @RequestBody @Validated CompetitionModule updateEntity) {
    CompetitionModule existingModule =
        competitionModuleService.findOne(updateEntity.getId()).orElseThrow(NotFoundException::new);
    updateEntity.setPath(existingModule.getPath());
    competitionModuleService.validateCompetitionId(updateEntity);
    competitionModuleService.populateCompetitionIdsForGroupWidgetModule(updateEntity, brand);
    competitionModuleService.updateMaxDisplayValue(updateEntity);
    return super.update(id, updateEntity);
  }

  @DeleteMapping("competition/{compId}/tab/{tabId}/module/{moduleId}")
  public ResponseEntity deleteTabModule(
      @PathVariable @NotEmpty String compId,
      @PathVariable @NotEmpty String tabId,
      @PathVariable @NotEmpty String moduleId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    CompetitionTab tab = competitionService.getCompetitionTab(compId, tabId, competition);
    List<CompetitionModule> modules =
        tab.getCompetitionModules().stream()
            .filter(m -> !m.getId().equals(moduleId))
            .collect(Collectors.toList());
    tab.setCompetitionModules(modules);
    competitionTabService.save(tab);
    return super.delete(moduleId);
  }

  @DeleteMapping("competition/{compId}/tab/{tabId}/subTab/{subTabId}/module/{moduleId}")
  public ResponseEntity deleteSubTabModule(
      @PathVariable @NotEmpty String compId,
      @PathVariable @NotEmpty String tabId,
      @PathVariable @NotEmpty String subTabId,
      @PathVariable @NotEmpty String moduleId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    CompetitionTab tab = competitionService.getCompetitionTab(compId, tabId, competition);
    CompetitionSubTab subTab = competitionService.getCompetitionSubTab(tabId, subTabId, tab);
    List<CompetitionModule> modules =
        subTab.getCompetitionModules().stream()
            .filter(m -> !m.getId().equals(moduleId))
            .collect(Collectors.toList());
    subTab.setCompetitionModules(modules);
    competitionSubTabService.save(subTab);
    return super.delete(moduleId);
  }

  private void validateSortedItemsSize(int sortedIdSize, int dbItemSize) {
    Assert.isTrue(
        sortedIdSize == dbItemSize,
        "There are "
            + dbItemSize
            + " items in db but specified only "
            + sortedIdSize
            + " item ids");
  }
}
