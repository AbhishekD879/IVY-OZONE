package com.ladbrokescoral.oxygen.bigcompetition.service;

import com.ladbrokescoral.oxygen.bigcompetition.TestUtil;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.SurfaceBetsModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.module.SurfaceBetsModuleServiceImpl;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SurfaceBetsServiceTest {

  private SurfaceBetsModuleServiceImpl surfaceBetsModuleService;

  @Before
  public void before() {
    surfaceBetsModuleService = new SurfaceBetsModuleServiceImpl();
  }

  @Test
  public void testSurfaceBetsFromCms() {

    CompetitionModule competitionModuleDto =
        TestUtil.deserializeWithJackson(
            "/competitionPromotionsService/SurfaceBetsModuleInput.json", CompetitionModule.class);
    SurfaceBetsModuleDto betsModuleDto = surfaceBetsModuleService.process(competitionModuleDto);
    Assert.assertNotNull(betsModuleDto);
  }
}
