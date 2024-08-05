package com.ladbrokescoral.oxygen.bigcompetition.service;

import com.ladbrokescoral.oxygen.bigcompetition.TestUtil;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.GroupModuleBrGroupDetailMapper;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.ParticipantMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.module.GroupModuleServiceImpl;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CompetitionErrorHandlingTest {
  @Mock CmsApiService cmsApiService;
  @Mock StatsCenterApiService statsCenterApiService;

  @Mock
  GroupModuleBrGroupDetailMapper groupModuleBrGroupDetailMapper =
      new GroupModuleBrGroupDetailMapper(new ParticipantMapper());

  @Mock SiteServeApiService siteServeApiService;

  GroupModuleService competitionGroupService;

  @Before
  public void setUp() {
    competitionGroupService =
        new GroupModuleServiceImpl(
            statsCenterApiService,
            groupModuleBrGroupDetailMapper,
            cmsApiService,
            siteServeApiService,
            "bma");
  }

  @Rule public ExpectedException expectedEx = ExpectedException.none();

  @Test
  public void testGroupModuleError() {
    expectedEx.expect(Exception.class);
    expectedEx.expectMessage(
        "Can't get data from stats center sportId = 1, areaId = 4, "
            + "compId = 3955, seasonId = 48238");

    CompetitionModule competitionModule =
        TestUtil.deserializeWithJackson(
            "/competitionGroupService/competitionModuleDtoGroupAllInpout.json",
            CompetitionModule.class);
    competitionGroupService.process(competitionModule);
  }
}
