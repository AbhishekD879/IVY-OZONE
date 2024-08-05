package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.api.entity.SvgSprite.INITIAL;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.BDDMockito.given;

import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataCFDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OddsBoostConfigDTO;
import com.ladbrokescoral.oxygen.cms.api.dto.SvgSpriteDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.test.context.junit4.SpringRunner;
import org.wildfly.common.Assert;

@RunWith(SpringRunner.class)
public class InitialDataServiceTest {

  @Mock SportCategoryPublicService sportCategoryService;
  @Mock ModularContentPublicService modularContentService;
  @Mock SeoPagePublicService seoPageService;
  @Mock FooterMenuPublicService footerMenuService;
  @Mock SportPublicService sportService;
  @Mock InitSignpostingPublicService initSignpostingService;
  @Mock StructurePublicService structureService;
  @Mock NavigationPointService navigationPointService;
  @Mock ExtraNavigationPointPublicService extraNavigationPointPublicService;
  @Mock BuildYourBetPublicService buildYourBetPublicService;
  @Mock BybTabAvailabilityService bybTabAvailabilityService;
  @Mock ConnectMenuPublicService connectMenuPublicService;
  @Mock HeaderContactMenuPublicService headerContactMenuService;
  @Mock OddsBoostConfigurationService oddsBoostConfigurationService;
  @Mock QuizPopupSettingPublicService quizPopupService;
  @Mock TimelineConfigPublicService timelineConfigService;
  @Mock VirtualSportPublicService virtualSportPublicService;
  @Mock private SvgImagePublicService svgImagePublicService;
  @Mock SeoAutoPagePublicService seoAutoPagePublicService;
  @Mock SegmentService segmentService;
  @Mock LuckyDipV2ConfigService luckyDipV2ConfigService;
  @InjectMocks private InitialDataService initialDataService;

  @Before
  public void setUp() throws Exception {
    given(oddsBoostConfigurationService.getPublicDTO(anyString()))
        .willReturn(new OddsBoostConfigDTO());

    given(svgImagePublicService.getSvgSprite(anyString(), eq(INITIAL.getSpriteName())))
        .willReturn(new SvgSpriteDto(INITIAL.getSpriteName(), "<svg/>"));

    given(svgImagePublicService.getSvgSprites(anyString(), anyList()))
        .willReturn(new SvgSpriteDto(INITIAL.getSpriteName(), "<svg/>"));
  }

  @Test
  public void testFindAllByBrandAndDeviceTypeWithDefaultDeviceType() {
    InitialDataCFDto initialDataCFDto =
        initialDataService.fetchCFInitialData("ladbrokes", "mobile");
    Assert.assertNotNull(initialDataCFDto);
  }

  @Test
  public void testFindAllByBrandAndDeviceTypeDesktopWithDefaultDeviceType() {

    OddsBoostConfigDTO dto = new OddsBoostConfigDTO();
    dto.setEnabled(true);
    given(oddsBoostConfigurationService.getPublicDTO(anyString())).willReturn(dto);
    InitialDataCFDto initialDataCFDto =
        initialDataService.fetchCFInitialData("ladbrokes", "Desktop");
    Assert.assertTrue(initialDataCFDto.getOddsBoost().isEnabled());
  }
}
