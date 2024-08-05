package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Competition;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionTab;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionService;
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
public class CompetitionTabs extends AbstractCrudController<CompetitionTab> {
  private CompetitionService competitionService;
  CompetitionTabService competitionTabService;

  @Autowired
  CompetitionTabs(
      CompetitionTabService competitionTabService, CompetitionService competitionService) {
    super(competitionTabService);
    this.competitionService = competitionService;
    this.competitionTabService = competitionTabService;
  }

  @PostMapping("competition/{id}/tab")
  public ResponseEntity create(
      @RequestBody @Validated CompetitionTab entity, @PathVariable @NotEmpty String id) {
    Competition competition = competitionService.getCompetitionByid(id);
    entity.setPathFromParent(competition);
    CompetitionTab tab = super.createEntity(entity);
    Assert.isTrue(null != tab, "Tab is not created");
    List<CompetitionTab> tabs =
        Optional.ofNullable(competition.getCompetitionTabs()).orElse(new ArrayList<>());
    tabs.add(tab);
    competition.setCompetitionTabs(tabs);
    competitionService.save(competition);
    return new ResponseEntity<>(tab, HttpStatus.CREATED);
  }

  @GetMapping("competition/{compId}/tab/{tabId}")
  public ResponseEntity readWithParentCompetition(
      @PathVariable @NotEmpty String compId, @PathVariable @NotEmpty String tabId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    CompetitionTab tab = competitionService.getCompetitionTab(compId, tabId, competition);
    populateCreatorAndUpdater(competition);
    populateCreatorAndUpdater(tab);
    competition.setCompetitionTabs(Arrays.asList(tab));
    return new ResponseEntity<>(competition, HttpStatus.OK);
  }

  @GetMapping("competitionTab")
  @Override
  public List<CompetitionTab> readAll() {
    return super.readAll();
  }

  @GetMapping("competitionTab/{id}")
  @Override
  public CompetitionTab read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping("competitionTab/{id}")
  @Override
  public CompetitionTab update(
      @PathVariable String id, @RequestBody @Validated CompetitionTab updateEntity) {
    CompetitionTab tab = super.crudService.findOne(id).orElseThrow(NotFoundException::new);

    updateEntity.setPathFromExistingEntity(tab);
    updateEntity.setCompetitionSubTabs(tab.getCompetitionSubTabs());
    updateEntity.setCompetitionModules(tab.getCompetitionModules());
    return super.update(id, updateEntity);
  }

  @PostMapping("competition/{compId}/tab/ordering")
  public ResponseEntity order(
      @RequestBody OrderDto newOrder, @PathVariable @NotEmpty String compId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    int sortedIdSize = newOrder.getOrder().size();
    int dbItemSize = competition.getCompetitionTabs().size();
    Assert.isTrue(
        sortedIdSize == dbItemSize,
        "There are "
            + dbItemSize
            + " items in db but specified only "
            + sortedIdSize
            + " item ids");
    List<CompetitionTab> sortedCollection =
        newOrder.getOrder().stream()
            .map(item -> super.crudService.findOne(item).get())
            .collect(Collectors.toList());
    competition.setCompetitionTabs(sortedCollection);
    competitionService.save(competition);
    return new ResponseEntity(HttpStatus.OK);
  }

  @DeleteMapping("competition/{compId}/tab/{tabId}")
  public ResponseEntity delete(
      @PathVariable @NotEmpty String compId, @PathVariable @NotEmpty String tabId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    List<CompetitionTab> newTabs =
        competition.getCompetitionTabs().stream()
            .filter(tab -> !tab.getId().equals(tabId))
            .collect(Collectors.toList());
    competition.setCompetitionTabs(newTabs);
    competitionService.save(competition);
    return super.delete(tabId);
  }
}
