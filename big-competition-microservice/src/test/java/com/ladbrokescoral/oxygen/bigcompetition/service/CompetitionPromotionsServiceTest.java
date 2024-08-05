package com.ladbrokescoral.oxygen.bigcompetition.service;

import static org.mockito.Mockito.when;

import com.fasterxml.jackson.core.type.TypeReference;
import com.ladbrokescoral.oxygen.bigcompetition.TestUtil;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.PromotionModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.module.PromotionModuleServiceImpl;
import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import com.ladbrokescoral.oxygen.cms.client.model.PromotionContainerDto;
import com.ladbrokescoral.oxygen.cms.client.model.PromotionV2Dto;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CompetitionPromotionsServiceTest {
  @Mock private CmsApiService cmsApiService;

  private PromotionModuleServiceImpl competitionPromotionService;

  @Before
  public void setUp() {
    competitionPromotionService = new PromotionModuleServiceImpl(cmsApiService, "bma");
  }

  @Test
  public void testGetCompetitionPromotions() {
    // Preparation
    PromotionContainerDto<PromotionV2Dto> promotionsData =
        TestUtil.deserializeWithJacksonToType(
            "/competitionPromotionsService/cmsPromotionsResponse.json",
            new TypeReference<PromotionContainerDto<PromotionV2Dto>>() {});
    when(cmsApiService.findPromotionsByBrandAndCompetitionId("bma", "5acb3263c9e77c0001aa69a1"))
        .thenReturn(Optional.ofNullable(promotionsData));

    Competition competition = new Competition();
    competition.setId("5acb3263c9e77c0001aa69a1");

    when(cmsApiService.findCompetitionByBrandAndUri("bma", "comp"))
        .thenReturn(Optional.of(competition));

    CompetitionModule competitionModule =
        TestUtil.deserializeWithJackson(
            "/competitionPromotionsService/promotionModuleInput.json", CompetitionModule.class);
    PromotionModuleDto expected =
        TestUtil.deserializeWithJackson(
            "/competitionPromotionsService/promotionModuleResult.json", PromotionModuleDto.class);
    Assert.assertNotNull(expected);
    expected.setPath("/comp/tab/module");

    PromotionModuleDto actual = competitionPromotionService.process(competitionModule);
    Assert.assertEquals("Changes at promotion structure", expected, actual);
  }
}
