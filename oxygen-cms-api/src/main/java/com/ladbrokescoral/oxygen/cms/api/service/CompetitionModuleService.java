package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.api.entity.CompetitionModuleType.GROUP_ALL;
import static com.ladbrokescoral.oxygen.cms.api.entity.CompetitionModuleType.GROUP_INDIVIDUAL;
import static com.ladbrokescoral.oxygen.cms.api.entity.CompetitionModuleType.GROUP_WIDGET;
import static com.ladbrokescoral.oxygen.cms.api.entity.CompetitionModuleType.NEXT_EVENTS_INDIVIDUAL;
import static com.ladbrokescoral.oxygen.cms.api.entity.CompetitionModuleType.RESULTS;
import static com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProviderImpl.DEFAULT_BRAND;

import com.ladbrokescoral.oxygen.betradar.client.entity.BrCompetitionSeason;
import com.ladbrokescoral.oxygen.betradar.client.entity.StatsCompetition;
import com.ladbrokescoral.oxygen.betradar.client.entity.StatsSeason;
import com.ladbrokescoral.oxygen.betradar.client.service.StatsCenterApiClient;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.CompetitionModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.CompetitionRepository;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.util.Assert;

@Component
public class CompetitionModuleService extends AbstractService<CompetitionModule> {

  private static final int RESULTS_MAX_DISPLAY = 7;
  private static final int MAX_DISPLAY = 10;
  private final CompetitionModuleRepository competitionModuleRepository;
  private final CompetitionRepository competitionRepository;

  private StatsCenterApiClient statsCenterApiClient;
  private SiteServeService siteServeService;

  @Autowired
  public CompetitionModuleService(
      CompetitionModuleRepository competitionModuleRepository,
      SiteServeService siteServeService,
      CompetitionRepository competitionRepository,
      StatsCenterApiClient statsCenterApiClient) {
    super(competitionModuleRepository);
    this.competitionModuleRepository = competitionModuleRepository;
    this.competitionRepository = competitionRepository;
    this.statsCenterApiClient = statsCenterApiClient;
    this.siteServeService = siteServeService;
  }

  @Override
  public List<CompetitionModule> findByBrand(String brand) {
    return competitionModuleRepository.findAll();
  }

  @Override
  public CompetitionModule prepareModelBeforeSave(CompetitionModule model) {
    Optional.ofNullable(model.getTypeId())
        .ifPresent(typeId -> siteServeService.isTypeIdValid(DEFAULT_BRAND, typeId));
    return model;
  }

  public BrCompetitionSeason getStatsCenterCompetitionSeason(Competition competition) {
    BrCompetitionSeason allCompetitions = retrieveBrCompetitionSeason(competition);

    return allCompetitions;
  }

  private BrCompetitionSeason retrieveBrCompetitionSeason(Competition competition) {
    Optional<BrCompetitionSeason> competitionSeason =
        statsCenterApiClient.getAllCompetitions(
            competition.getCategoryId(), competition.getClazzId(), competition.getTypeId());
    Assert.isTrue(competitionSeason.isPresent(), "Can't get competition from stats center");
    BrCompetitionSeason brCompetitionSeason = competitionSeason.get();
    Assert.isTrue(
        Optional.ofNullable(brCompetitionSeason.getAllCompetitions()).isPresent(),
        String.format(
            "There aren't competition/groups for competition - typeId=%d, categoryId=%d, clazzId=%d   %n Stats center - %s",
            competition.getTypeId(),
            competition.getCategoryId(),
            competition.getClazzId(),
            brCompetitionSeason.toString()));
    return filterKhockout(brCompetitionSeason);
  }

  private BrCompetitionSeason filterKhockout(BrCompetitionSeason brCompetitionSeason) {
    List<StatsCompetition> groups =
        brCompetitionSeason.getAllCompetitions().stream()
            .filter(c -> !c.getName().contains("Knockout"))
            .collect(Collectors.toList());
    brCompetitionSeason.setAllCompetitions(groups);
    return brCompetitionSeason;
  }

  private List<StatsSeason> retrieveStatsSeasons(BrCompetitionSeason competitionSeason) {
    Integer sportId = competitionSeason.getSportId();
    Integer areaId = competitionSeason.getAreaId();
    Integer competitionId = competitionSeason.getCompetitionId();
    Optional<List<StatsSeason>> allSeasons =
        statsCenterApiClient.getAllSeasons(sportId, areaId, competitionId);
    Assert.isTrue(
        allSeasons.isPresent() && !allSeasons.get().isEmpty(),
        "Can't get seasons from stats center");
    return allSeasons.get();
  }

  public void populateCompetitionIdsForGroupWidgetModule(CompetitionModule updateEntity) {
    String compUri = "/" + updateEntity.getPath().split("/")[1];
    Optional<Competition> competition = competitionRepository.findByUri(compUri);
    Assert.isTrue(
        competition.isPresent(), String.format("Can't find competition by uri %s", compUri));
    populateCompetitionIdsForGroupWidgetModule(updateEntity, competition.get());
  }

  public void populateCompetitionIdsForGroupWidgetModule(
      CompetitionModule competitionModule, Competition competition) {
    if (GROUP_WIDGET.equals(competitionModule.getType())) {
      CompetitionGroupModuleData groupModuleData = competitionModule.getGroupModuleData();
      Assert.isTrue(null != groupModuleData, "Group widget should have a group module data");
      BrCompetitionSeason allCompetitions = retrieveBrCompetitionSeason(competition);
      List<Integer> allGroupIds =
          allCompetitions.getAllCompetitions().stream()
              .map(StatsCompetition::getId)
              .collect(Collectors.toList());
      competitionModule.getGroupModuleData().setCompetitionIds(allGroupIds);
    }
  }

  public void populateCompetitionIdsForGroupWidgetModule(
      CompetitionModule updateEntity, String brand) {
    String compUri = "/" + updateEntity.getPath().split("/")[1];
    Optional<Competition> competition = competitionRepository.findByBrandAndUri(brand, compUri);
    Assert.isTrue(
        competition.isPresent(), String.format("Can't find competition by uri %s", compUri));
    populateCompetitionIdsForGroupWidgetModule(updateEntity, competition.get());
  }

  public void validateCompetitionId(CompetitionModule competitionModule) {
    if (competitionModule.getType() == null) {
      throw new ValidationException("Module type can't be null");
    }
    if ((GROUP_INDIVIDUAL.equals(competitionModule.getType())
            || GROUP_ALL.equals(competitionModule.getType())
            || GROUP_WIDGET.equals(competitionModule.getType()))
        && !Optional.ofNullable(competitionModule.getGroupModuleData()).isPresent()) {
      throw new ValidationException("No group data in group module");
    }
    if ((GROUP_INDIVIDUAL.equals(competitionModule.getType())
            || GROUP_ALL.equals(competitionModule.getType()))
        && competitionModule.getGroupModuleData().getCompetitionId() == null) {
      throw new ValidationException("CompetitionId can't be null for Group Individual or All");
    }
    if ((GROUP_ALL.equals(competitionModule.getType())
            || NEXT_EVENTS_INDIVIDUAL.equals(competitionModule.getType()))
        && !Optional.ofNullable(competitionModule.getEventIds()).isPresent()) {
      throw new ValidationException(
          String.format(
              "Field eventIds is required for %s module %s %s",
              competitionModule.getType().toString(),
              competitionModule.getId(),
              competitionModule.getName()));
    }
    if (RESULTS.equals(competitionModule.getType())
        && competitionModule.getResultModuleSeasonId() == null) {
      throw new ValidationException("\"resultModuleSeasonId\" can't be null for Result module");
    }
  }

  public void updateMaxDisplayValue(CompetitionModule competitionModule) {
    int maxDisplay = calculateMaxDisplay(competitionModule);
    competitionModule.setMaxDisplay(maxDisplay);
  }

  private int calculateMaxDisplay(CompetitionModule competitionModule) {
    if (RESULTS.equals(competitionModule.getType()) && competitionModule.getMaxDisplay() == 0) {
      return RESULTS_MAX_DISPLAY;
    } else {
      return competitionModule.getMaxDisplay() == 0
          ? MAX_DISPLAY
          : competitionModule.getMaxDisplay();
    }
  }

  /**
   * Is invoked when competitionTab is being created or updated and needs to update all its modules
   */
  public void populatePathAndSave(CompetitionTab competitionTab, CompetitionModule module) {
    module.setPathFromParentCompetitionTab(competitionTab);
    save(module);
  }

  /**
   * Is invoked when competitionSubTab is being created or updated and needs to update all its
   * modules
   */
  public void populatePathAndSave(CompetitionSubTab competitionSubTab, CompetitionModule module) {
    module.setPathFromParentCompetitionSubTab(competitionSubTab);
    save(module);
  }

  public List<CompetitionModule> findCompetitionModulesByType(
      CompetitionModuleType competitionModuleType) {
    return competitionModuleRepository.findByType(competitionModuleType);
  }
}
