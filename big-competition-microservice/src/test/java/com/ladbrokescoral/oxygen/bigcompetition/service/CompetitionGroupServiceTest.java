package com.ladbrokescoral.oxygen.bigcompetition.service;

import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.betradar.client.entity.ResultsTable;
import com.ladbrokescoral.oxygen.bigcompetition.TestUtil;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.GroupModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.statsCenter.GroupModuleBrGroupDetailDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.GroupModuleBrGroupDetailMapper;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.ParticipantMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.module.GroupModuleServiceImpl;
import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionParticipant;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CompetitionGroupServiceTest {
  @Mock CmsApiService cmsApiService;
  @Mock StatsCenterApiService statsCenterApiClient;
  @Mock SiteServeApiService siteServeApiService;
  GroupModuleBrGroupDetailMapper groupModuleBrGroupDetailMapper =
      new GroupModuleBrGroupDetailMapper(new ParticipantMapper());

  GroupModuleServiceImpl competitionGroupService;

  @Before
  public void setUp() throws Exception {
    competitionGroupService =
        new GroupModuleServiceImpl(
            statsCenterApiClient,
            groupModuleBrGroupDetailMapper,
            cmsApiService,
            siteServeApiService,
            "bma");
  }

  @Test
  public void testGetCompetitionParticipants() {
    Competition competition =
        TestUtil.deserializeWithJackson(
            "/competitionParticipantService/competition_from_cms.json", Competition.class);
    when(cmsApiService.findCompetitionByBrandAndUri("bma", "world-cup"))
        .thenReturn(Optional.of(competition));
    List<CompetitionParticipant> competitionParticipants =
        competitionGroupService.getCompetitionParticipants("bma", "world-cup");
    Assert.assertEquals(
        "Method should return participant  counries list",
        "Spain",
        competitionParticipants.get(0).getObName());
  }

  @Test
  public void testToDto() {
    List<ResultsTable> resultsTables =
        TestUtil.deserializeListWithJackson(
            "/competitionParticipantService/betradar_result_table.json", ResultsTable.class);
    System.out.println(resultsTables);
    Competition competition =
        TestUtil.deserializeWithJackson(
            "/competitionParticipantService/competition_from_cms.json", Competition.class);
    when(cmsApiService.findCompetitionByBrandAndUri("bma", "world-cup"))
        .thenReturn(Optional.of(competition));
    List<CompetitionParticipant> competitionParticipants =
        competitionGroupService.getCompetitionParticipants("bma", "world-cup");
    List<GroupModuleBrGroupDetailDto> groupModuleBrGroupDetailDtos =
        groupModuleBrGroupDetailMapper.toDto(resultsTables, competitionParticipants);
    List<GroupModuleBrGroupDetailDto> expected =
        TestUtil.deserializeListWithJackson(
            "/competitionGroupService/groupModuleDataExpected.json",
            GroupModuleBrGroupDetailDto.class);
    Assert.assertEquals(
        TestUtil.serializeWithJackson(expected),
        TestUtil.serializeWithJackson(groupModuleBrGroupDetailDtos));
  }

  @Test
  public void testPopulateGroupWidget() {
    // Preparation
    Competition competition =
        TestUtil.deserializeWithJackson(
            "/competitionGroupService/competititons_for_widget.json", Competition.class);
    when(cmsApiService.findCompetitionByBrandAndUri("bma", "world-cup"))
        .thenReturn(Optional.of(competition));

    when(statsCenterApiClient.getResultTables(1, 4, 3954, 48238))
        .thenReturn(
            Optional.ofNullable(
                TestUtil.deserializeListWithJackson(
                    "/competitionGroupService/statsCenterGroups/groupA.json", ResultsTable.class)));
    when(statsCenterApiClient.getResultTables(1, 4, 3955, 48238))
        .thenReturn(
            Optional.ofNullable(
                TestUtil.deserializeListWithJackson(
                    "/competitionGroupService/statsCenterGroups/groupB.json", ResultsTable.class)));
    when(statsCenterApiClient.getResultTables(1, 4, 3956, 48238))
        .thenReturn(
            Optional.ofNullable(
                TestUtil.deserializeListWithJackson(
                    "/competitionGroupService/statsCenterGroups/groupC.json", ResultsTable.class)));
    when(statsCenterApiClient.getResultTables(1, 4, 3957, 48238))
        .thenReturn(
            Optional.ofNullable(
                TestUtil.deserializeListWithJackson(
                    "/competitionGroupService/statsCenterGroups/groupD.json", ResultsTable.class)));
    when(statsCenterApiClient.getResultTables(1, 4, 3958, 48238))
        .thenReturn(
            Optional.ofNullable(
                TestUtil.deserializeListWithJackson(
                    "/competitionGroupService/statsCenterGroups/groupE.json", ResultsTable.class)));
    when(statsCenterApiClient.getResultTables(1, 4, 3959, 48238))
        .thenReturn(
            Optional.ofNullable(
                TestUtil.deserializeListWithJackson(
                    "/competitionGroupService/statsCenterGroups/groupF.json", ResultsTable.class)));
    when(statsCenterApiClient.getResultTables(1, 4, 3960, 48238))
        .thenReturn(
            Optional.ofNullable(
                TestUtil.deserializeListWithJackson(
                    "/competitionGroupService/statsCenterGroups/groupG.json", ResultsTable.class)));
    when(statsCenterApiClient.getResultTables(1, 4, 3961, 48238))
        .thenReturn(
            Optional.ofNullable(
                TestUtil.deserializeListWithJackson(
                    "/competitionGroupService/statsCenterGroups/groupH.json", ResultsTable.class)));

    CompetitionModule competitionModule =
        TestUtil.deserializeWithJackson(
            "/competitionGroupService/competitionModuleDtoInput.json", CompetitionModule.class);
    GroupModuleDto actualResult = competitionGroupService.process(competitionModule);
    GroupModuleDto expectedResult =
        TestUtil.deserializeWithJackson(
            "/competitionGroupService/competitionModuleDtoOut.json", GroupModuleDto.class);
    expectedResult.setPath("/world-cup");
    Assert.assertEquals("Data processing is incorrect", expectedResult, actualResult);
  }

  @Test
  public void testPopulateGroupAll() {
    when(siteServeApiService.getWholeEventToOutcomeForMarket("120352920,120352921", true))
        .thenReturn(
            Optional.ofNullable(
                TestUtil.deserializeListWithJackson(
                    "/competitionGroupService/SSResponse/ssEventToOutcomeForMarket.json",
                    Event.class)));
    when(statsCenterApiClient.getResultTables(1, 4, 3955, 48238))
        .thenReturn(
            Optional.ofNullable(
                TestUtil.deserializeListWithJackson(
                    "/competitionGroupService/statsCenterGroups/groupB.json", ResultsTable.class)));
    Competition competition =
        TestUtil.deserializeWithJackson(
            "/competitionGroupService/competitionGroupAllInput.json", Competition.class);
    when(cmsApiService.findCompetitionByBrandAndUri("bma", "world-cup"))
        .thenReturn(Optional.of(competition));

    CompetitionModule competitionModule =
        TestUtil.deserializeWithJackson(
            "/competitionGroupService/competitionModuleDtoGroupAllInpout.json",
            CompetitionModule.class);
    GroupModuleDto actualResult = competitionGroupService.process(competitionModule);
    GroupModuleDto expectedResult =
        TestUtil.deserializeWithJackson(
            "/competitionGroupService/competitionModuleDtoGroupAllOutput.json",
            GroupModuleDto.class);
    Assert.assertEquals(
        "Data processing is incorrect",
        TestUtil.serializeWithJackson(expectedResult),
        TestUtil.serializeWithJackson(actualResult));
  }

  @Test
  public void testPopulateGroupAllEmptyMarkets() {
    when(statsCenterApiClient.getResultTables(1, 4, 3955, 48238))
        .thenReturn(
            Optional.ofNullable(
                TestUtil.deserializeListWithJackson(
                    "/competitionGroupService/statsCenterGroups/groupB.json", ResultsTable.class)));
    Competition competition =
        TestUtil.deserializeWithJackson(
            "/competitionGroupService/competitionGroupAllInput.json", Competition.class);
    when(cmsApiService.findCompetitionByBrandAndUri("bma", "world-cup"))
        .thenReturn(Optional.of(competition));

    CompetitionModule competitionModule =
        TestUtil.deserializeWithJackson(
            "/competitionGroupService/testNoMarkets/competitionModuleDtoGroupAllInpoutNoMarkets.json",
            CompetitionModule.class);
    GroupModuleDto actualResult = competitionGroupService.process(competitionModule);
    GroupModuleDto expectedResult =
        TestUtil.deserializeWithJackson(
            "/competitionGroupService/testNoMarkets/competitionModuleDtoGroupAllOutputNoMarkets.json",
            GroupModuleDto.class);
    Assert.assertEquals(
        "Data processing is incorrect",
        TestUtil.serializeWithJackson(expectedResult),
        TestUtil.serializeWithJackson(actualResult));
  }
}
