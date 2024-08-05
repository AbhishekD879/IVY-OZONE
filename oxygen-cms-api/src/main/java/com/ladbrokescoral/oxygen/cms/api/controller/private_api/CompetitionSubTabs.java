package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Competition;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionSubTab;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionTab;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
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
public class CompetitionSubTabs extends AbstractCrudController<CompetitionSubTab> {
  private CompetitionService competitionService;
  private CompetitionTabService competitionTabService;

  @Autowired
  CompetitionSubTabs(
      CompetitionSubTabService competitionSubTabService,
      CompetitionService competitionService,
      CompetitionTabService competitionTabService) {
    super(competitionSubTabService);
    this.competitionService = competitionService;
    this.competitionTabService = competitionTabService;
  }

  @PostMapping("competition/{compId}/tab/{tabId}/subTab")
  public ResponseEntity create(
      @RequestBody @Validated CompetitionSubTab entity,
      @PathVariable @NotEmpty String compId,
      @PathVariable @NotEmpty String tabId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    CompetitionTab competitionTab =
        competitionService.getCompetitionTab(compId, tabId, competition);
    entity.setPathFromParent(competitionTab);
    CompetitionSubTab competitionSubTab = super.createEntity(entity);
    List<CompetitionSubTab> subTabs =
        Optional.ofNullable(competitionTab.getCompetitionSubTabs()).orElse(new ArrayList<>());
    subTabs.add(competitionSubTab);
    competitionTab.setCompetitionSubTabs(subTabs);
    competitionTabService.save(competitionTab);
    return new ResponseEntity<>(competitionSubTab, HttpStatus.CREATED);
  }

  @GetMapping("competition/{compId}/tab/{tabId}/subTab/{subTabId}")
  public ResponseEntity readWithParentCompetition(
      @PathVariable @NotEmpty String compId,
      @PathVariable @NotEmpty String tabId,
      @PathVariable @NotEmpty String subTabId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    CompetitionTab tab = competitionService.getCompetitionTab(compId, tabId, competition);
    CompetitionSubTab subTab = competitionService.getCompetitionSubTab(tabId, subTabId, tab);
    populateCreatorAndUpdater(competition);
    populateCreatorAndUpdater(tab);
    populateCreatorAndUpdater(subTab);
    competition.setCompetitionTabs(Arrays.asList(tab));
    tab.setCompetitionSubTabs(Arrays.asList(subTab));
    return new ResponseEntity<>(competition, HttpStatus.OK);
  }

  @GetMapping("competitionSubTab")
  @Override
  public List<CompetitionSubTab> readAll() {
    return super.readAll();
  }

  @GetMapping("competitionSubTab/{id}")
  @Override
  public CompetitionSubTab read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping("competitionSubTab/{id}")
  @Override
  public CompetitionSubTab update(
      @PathVariable String id, @RequestBody @Validated CompetitionSubTab updateEntity) {
    CompetitionSubTab subTab = super.crudService.findOne(id).orElseThrow(NotFoundException::new);

    updateEntity.setPathFromExistingEntity(subTab);
    updateEntity.setCompetitionModules(subTab.getCompetitionModules());
    return super.update(id, updateEntity);
  }

  @PostMapping("competition/{compId}/tab/{tabId}/subTab/ordering")
  public ResponseEntity order(
      @RequestBody OrderDto newOrder,
      @PathVariable @NotEmpty String compId,
      @PathVariable @NotEmpty String tabId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    CompetitionTab tab = competitionService.getCompetitionTab(compId, tabId, competition);
    int sortedIdSize = newOrder.getOrder().size();
    int dbItemSize = tab.getCompetitionSubTabs().size();
    Assert.isTrue(
        sortedIdSize == dbItemSize,
        "There are "
            + dbItemSize
            + " items in db but specified only "
            + sortedIdSize
            + " item ids");
    List<CompetitionSubTab> sortedCollection =
        newOrder.getOrder().stream()
            .map(item -> super.crudService.findOne(item).get())
            .collect(Collectors.toList());
    tab.setCompetitionSubTabs(sortedCollection);
    competitionTabService.save(tab);
    return new ResponseEntity(HttpStatus.OK);
  }

  @DeleteMapping("competition/{compId}/tab/{tabId}/subTab/{subTabId}")
  public ResponseEntity delete(
      @PathVariable @NotEmpty String compId,
      @PathVariable @NotEmpty String tabId,
      @PathVariable @NotEmpty String subTabId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    CompetitionTab tab = competitionService.getCompetitionTab(compId, tabId, competition);
    List<CompetitionSubTab> leftSubTabs =
        tab.getCompetitionSubTabs().stream()
            .filter(subTab -> !subTab.getId().equals(subTabId))
            .collect(Collectors.toList());
    tab.setCompetitionSubTabs(leftSubTabs);
    competitionTabService.save(tab);
    return super.delete(subTabId);
  }
}
