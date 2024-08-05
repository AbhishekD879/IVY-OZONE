package com.ladbrokescoral.oxygen.bigcompetition.service;

import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.betradar.client.entity.SeasonMatches;
import com.ladbrokescoral.oxygen.bigcompetition.TestUtil;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.ResultsModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.ParticipantMapper;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.ResultsModuleMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.module.ResultModuleServiceImpl;
import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import java.util.Arrays;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class ResultModuleServiceTest {

  @Mock StatsCenterApiService statsCenterApiService;
  @Mock CmsApiService cmsApiService;
  private ResultsModuleMapper mapper = new ResultsModuleMapper(new ParticipantMapper());

  private ResultModuleServiceImpl service;
  private final int skip = 0;
  private final int limit = 200;
  private final String brand = "bma";

  @Before
  public void setUp() {
    service =
        new ResultModuleServiceImpl(
            statsCenterApiService, mapper, cmsApiService, skip, limit, brand);
  }

  @Test
  public void testCompetitionResultModule() {

    SeasonMatches[] seasonMatches =
        TestUtil.deserializeWithJackson(
            "/competitionResultService/seasonMatches_stats-center.json", SeasonMatches[].class);

    Competition competition =
        TestUtil.deserializeWithJackson(
            "/competitionResultService/competition_cms.json", Competition.class);

    when(statsCenterApiService.getSeasonMatches(41198, skip, limit))
        .thenReturn(Optional.of(Arrays.asList(seasonMatches)));

    when(cmsApiService.findCompetitionByBrandAndUri(Mockito.any(), Mockito.any()))
        .thenReturn(Optional.of(competition));

    CompetitionModule competitionModule =
        TestUtil.deserializeWithJackson(
            "/competitionResultService/competitionModuleDto.json", CompetitionModule.class);

    ResultsModuleDto actualResult = (ResultsModuleDto) service.process(competitionModule);

    ResultsModuleDto expectedResult =
        TestUtil.deserializeWithJackson(
            "/competitionResultService/competitionModuleDtoResult.json", ResultsModuleDto.class);
    Assert.assertEquals("Data processing is incorrect", expectedResult, actualResult);
  }
}
