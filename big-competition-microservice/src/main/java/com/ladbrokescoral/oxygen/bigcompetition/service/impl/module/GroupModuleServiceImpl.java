package com.ladbrokescoral.oxygen.bigcompetition.service.impl.module;

import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.betradar.client.entity.ResultsTable;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.GroupModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.group.CompetitionMarketDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.group.GroupModuleDataDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.MarketDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.OutcomeDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.statsCenter.GroupModuleBrGroupDetailDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.GroupModuleBrGroupDetailMapper;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.SiteServeEventDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.module.GroupModuleDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.CmsApiService;
import com.ladbrokescoral.oxygen.bigcompetition.service.GroupModuleService;
import com.ladbrokescoral.oxygen.bigcompetition.service.SiteServeApiService;
import com.ladbrokescoral.oxygen.bigcompetition.service.StatsCenterApiService;
import com.ladbrokescoral.oxygen.bigcompetition.util.Utils;
import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModuleType;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionParticipant;
import java.util.*;
import java.util.stream.Collectors;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.Assert;

@Service
// @Slf4j
public class GroupModuleServiceImpl implements GroupModuleService {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  private final StatsCenterApiService statsCenterApiService;
  private final GroupModuleBrGroupDetailMapper groupModuleBrGroupDetailMapper;
  private final CmsApiService cmsApiService;
  private final SiteServeApiService siteServeApiService;
  private final String brand;

  @Autowired
  public GroupModuleServiceImpl(
      @Qualifier("statsCenterApiServiceImpl") StatsCenterApiService statsCenterApiService,
      GroupModuleBrGroupDetailMapper groupModuleBrGroupDetailMapper,
      CmsApiService cmsApiService,
      SiteServeApiService siteServeApiService,
      @Value("${cms.brand}") String brand) {
    this.statsCenterApiService = statsCenterApiService;
    this.groupModuleBrGroupDetailMapper = groupModuleBrGroupDetailMapper;
    this.cmsApiService = cmsApiService;
    this.siteServeApiService = siteServeApiService;
    this.brand = brand;
  }

  @Override
  public GroupModuleDto process(CompetitionModule module) {
    GroupModuleDto competitionModuleDto = GroupModuleDtoMapper.INSTANCE.toDto(module);
    GroupModuleDataDto groupModuleData = competitionModuleDto.getGroupModuleData();
    CompetitionModuleType type = competitionModuleDto.getType();

    List<ResultsTable> brResultTable = getResultsTable(groupModuleData, type);
    List<CompetitionParticipant> competitionParticipants =
        getCompetitionParticipants(brand, competitionModuleDto.getCompetitionUriFromPath());
    List<GroupModuleBrGroupDetailDto> groupModuleBrGroupDetailDtos =
        groupModuleBrGroupDetailMapper.toDto(brResultTable, competitionParticipants);
    competitionModuleDto
        .getGroupModuleData()
        .setGroupModuleBrGroupDetailDtos(groupModuleBrGroupDetailDtos);
    return addEventsWithOutcomes(competitionModuleDto);
  }

  private GroupModuleDto addEventsWithOutcomes(GroupModuleDto competitionModuleDto) {
    if (competitionModuleDto.getType().equals(CompetitionModuleType.GROUP_ALL)) {
      List<GroupModuleBrGroupDetailDto> groupModuleBrGroupDetailDtos =
          competitionModuleDto.getGroupModuleData().getGroupModuleBrGroupDetailDtos();
      Utils.newRelicLogTransaction("/SS-getWholeEventToOutcomeForMarket");
      String marketIds =
          competitionModuleDto.getMarkets().stream()
              .map(CompetitionMarketDto::getMarketId)
              .collect(Collectors.joining(","));
      if (!marketIds.isEmpty()) {
        Optional<List<Event>> events =
            siteServeApiService.getWholeEventToOutcomeForMarket(marketIds, true);
        Assert.isTrue(
            events.isPresent(),
            String.format("Can't find an event that contains markets %s", marketIds));
        List<EventDto> eventDtos = mapSSEventsToEventDto(events.get());
        GroupModuleBrGroupDetailDto groupModuleBrDto =
            groupModuleBrGroupDetailDtos.get(0); // only one team for now
        List<String> teamNamesOrdered = getGroupTeamNameOrdered(groupModuleBrDto);
        eventDtos.forEach(eventDto -> sortMarketsAndOutcomes(teamNamesOrdered, eventDto));
        groupModuleBrDto.setSsEvents(eventDtos); // expect only one group
      }
    }
    return competitionModuleDto;
  }

  private void sortMarketsAndOutcomes(List<String> teamNamesOrdered, EventDto eventDto) {
    List<MarketDto> markets = eventDto.getMarkets();
    Assert.isTrue(
        Optional.ofNullable(markets).isPresent() && !markets.isEmpty(),
        String.format("Can't find markets at event %s", eventDto.getId()));
    List<MarketDto> sortedMarketDtos =
        markets.stream()
            .sorted(Comparator.comparing(MarketDto::getDisplayOrder))
            .map(
                marketDto -> {
                  sortOutcomes(teamNamesOrdered, marketDto);
                  return marketDto;
                })
            .collect(Collectors.toList());
    eventDto.setMarkets(sortedMarketDtos);
  }

  private void sortOutcomes(List<String> teamNamesOrdered, MarketDto m) {
    List<OutcomeDto> outcomes = m.getOutcomes();
    Assert.isTrue(
        Optional.ofNullable(outcomes).isPresent() && !outcomes.isEmpty(),
        String.format("Can't find outcomes at market %s", m.getId()));
    Map<String, OutcomeDto> outcomeMap =
        outcomes.stream().collect(Collectors.toMap(OutcomeDto::getName, o -> o));
    List<OutcomeDto> sortedOutcomes = sortOutcomes(teamNamesOrdered, outcomeMap);
    m.setOutcomes(sortedOutcomes);
  }

  private List<OutcomeDto> sortOutcomes(
      List<String> teamNamesOrdered, Map<String, OutcomeDto> outcomeMap) {
    return teamNamesOrdered.stream()
        .map(
            teamName -> {
              OutcomeDto outcomeDto = outcomeMap.get(teamName);
              Assert.isTrue(
                  outcomeDto != null,
                  String.format(
                      "Can't make mapping %s with outcomes %s",
                      teamName, outcomeMap.keySet().toString()));
              return outcomeDto;
            })
        .collect(Collectors.toList());
  }

  private List<EventDto> mapSSEventsToEventDto(List<Event> events) {
    return events.stream()
        .map(SiteServeEventDtoMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }

  private List<String> getGroupTeamNameOrdered(GroupModuleBrGroupDetailDto groupModuleBrDto) {
    return groupModuleBrDto.getTeams().stream()
        .map(t -> t.getObName().trim())
        .collect(Collectors.toList());
  }

  private List<ResultsTable> getResultsTable(
      GroupModuleDataDto groupModuleData, CompetitionModuleType type) {
    Integer sportId = groupModuleData.getSportId();
    Integer areaId = groupModuleData.getAreaId();
    Integer competitionId = groupModuleData.getCompetitionId();
    List<Integer> competitionIds = groupModuleData.getCompetitionIds();
    Integer seasonId = groupModuleData.getSeasonId();
    List<ResultsTable> resultTables = new ArrayList<>();
    if (type.equals(CompetitionModuleType.GROUP_WIDGET)) {
      resultTables =
          processGroupWidgetModule(sportId, areaId, competitionIds, seasonId, resultTables);
    }
    if (type.equals(CompetitionModuleType.GROUP_INDIVIDUAL)
        || type.equals(CompetitionModuleType.GROUP_ALL)) {
      resultTables = processSingleGroup(sportId, areaId, competitionId, seasonId);
    }
    return resultTables;
  }

  private List<ResultsTable> processSingleGroup(
      Integer sportId, Integer areaId, Integer competitionId, Integer seasonId) {
    String message =
        String.format(
            "Can't get data from stats center sportId = %d, areaId = %d, compId = %d, seasonId = %d",
            sportId, areaId, competitionId, seasonId);
    Assert.isTrue(
        null != sportId && null != areaId && null != competitionId && null != seasonId, message);
    Optional<List<ResultsTable>> group =
        statsCenterApiService.getResultTables(sportId, areaId, competitionId, seasonId);
    Assert.isTrue(group.isPresent(), message);
    return group.get();
  }

  private List<ResultsTable> processGroupWidgetModule(
      Integer sportId,
      Integer areaId,
      List<Integer> competitionIds,
      Integer seasonId,
      List<ResultsTable> resultTables) {
    Assert.isTrue(competitionIds != null, "CompetitionIds can't be null");
    competitionIds.forEach(
        compId -> {
          Optional<List<ResultsTable>> group =
              statsCenterApiService.getResultTables(sportId, areaId, compId, seasonId);
          if (!group.isPresent()) {
            ASYNC_LOGGER.warn(
                String.format(
                    "Can't get data from stats center sportId = %d, areaId = %d, compId = %d, seasonId = %d",
                    sportId, areaId, compId, seasonId));
          } else {
            group.ifPresent(resultTables::addAll);
          }
        });
    return resultTables;
  }

  public List<CompetitionParticipant> getCompetitionParticipants(
      String brand, String competitionUriFromPath) {
    Optional<Competition> competitionByUri =
        cmsApiService.findCompetitionByBrandAndUri(brand, competitionUriFromPath);
    Assert.isTrue(competitionByUri.isPresent(), "Can't find competition by url");
    return competitionByUri.get().getCompetitionParticipants();
  }
}
