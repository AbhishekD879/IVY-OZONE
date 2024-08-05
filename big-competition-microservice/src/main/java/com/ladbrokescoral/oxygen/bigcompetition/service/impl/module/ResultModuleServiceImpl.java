package com.ladbrokescoral.oxygen.bigcompetition.service.impl.module;

import com.ladbrokescoral.oxygen.betradar.client.entity.SeasonMatches;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.ResultsModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.results.ResultsModuleDataDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.ResultsModuleMapper;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.module.ResultsModuleDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.CmsApiService;
import com.ladbrokescoral.oxygen.bigcompetition.service.ResultModuleService;
import com.ladbrokescoral.oxygen.bigcompetition.service.StatsCenterApiService;
import com.ladbrokescoral.oxygen.bigcompetition.util.Utils;
import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionParticipant;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.Assert;

@Service
// @Slf4j
public class ResultModuleServiceImpl implements ResultModuleService {

  private final StatsCenterApiService statsCenterApiService;
  private final ResultsModuleMapper mapper;
  private final CmsApiService cmsApiService;
  private final Integer skip;
  private final Integer limit;
  private final String brand;

  @Autowired
  public ResultModuleServiceImpl(
      @Qualifier("statsCenterApiServiceImpl") StatsCenterApiService statsCenterApiService,
      ResultsModuleMapper mapper,
      CmsApiService cmsApiService,
      @Value("${statsCenter.season.matches.skip}") Integer skip,
      @Value("${statsCenter.season.matches.limit}") Integer limit,
      @Value("${cms.brand}") String brand) {
    this.statsCenterApiService = statsCenterApiService;
    this.mapper = mapper;
    this.cmsApiService = cmsApiService;
    this.skip = skip;
    this.limit = limit;
    this.brand = brand;
  }

  @Override
  public ResultsModuleDto process(CompetitionModule module) {
    ResultsModuleDto moduleDto = ResultsModuleDtoMapper.INSTANCE.toDto(module);

    List<SeasonMatches> seasonMatches = getSeasonMatches(module.getResultModuleSeasonId());
    List<CompetitionParticipant> participants =
        getCompetitionParticipants(brand, moduleDto.getCompetitionUriFromPath());
    List<ResultsModuleDataDto> resultsModuleDataDtos = mapper.toDto(seasonMatches, participants);
    Assert.isTrue(
        !resultsModuleDataDtos.isEmpty(),
        String.format("Can't get data for result module - %s ", module.getId()));
    moduleDto.getResults().addAll(resultsModuleDataDtos);
    return moduleDto;
  }

  private List<SeasonMatches> getSeasonMatches(Integer resultModuleSeasonId) {
    Utils.newRelicLogTransaction("/StatsCenter-getResultModuleSeasonId");
    return statsCenterApiService
        .getSeasonMatches(resultModuleSeasonId, skip, limit)
        .orElse(Collections.emptyList());
  }

  public List<CompetitionParticipant> getCompetitionParticipants(
      String brand, String competitionUriFromPath) {
    Optional<Competition> competitionByUri =
        cmsApiService.findCompetitionByBrandAndUri(brand, competitionUriFromPath);
    Assert.isTrue(competitionByUri.isPresent(), "Can't find competition by url");
    return competitionByUri.get().getCompetitionParticipants();
  }
}
