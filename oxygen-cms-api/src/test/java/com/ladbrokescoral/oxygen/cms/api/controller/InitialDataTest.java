package com.ladbrokescoral.oxygen.cms.api.controller;

import static com.ladbrokescoral.oxygen.cms.api.controller.ApiConstants.CMS_API;
import static com.ladbrokescoral.oxygen.cms.api.entity.SvgSprite.INITIAL;
import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.not;
import static org.mockito.BDDMockito.given;
import static org.mockito.Matchers.anyString;
import static org.mockito.Matchers.eq;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.Users;
import com.ladbrokescoral.oxygen.cms.api.controller.public_api.InitialDataApi;
import com.ladbrokescoral.oxygen.cms.api.dto.ConnectMenuDto;
import com.ladbrokescoral.oxygen.cms.api.dto.HeaderContactMenuDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OddsBoostConfigDTO;
import com.ladbrokescoral.oxygen.cms.api.dto.QuizPopupSettingDto;
import com.ladbrokescoral.oxygen.cms.api.dto.StructureDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SvgSpriteDto;
import com.ladbrokescoral.oxygen.cms.api.dto.TimelineGeneralConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      Users.class,
      AuthenticationService.class,
      InitialDataApi.class,
      InitialDataService.class,
      ConnectMenuPublicService.class,
      FooterMenuPublicService.class,
      ExtraNavigationPointPublicService.class,
      LuckyDipV2ConfigService.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class InitialDataTest {

  @Autowired private MockMvc mockMvc;
  @MockBean private UserService userServiceMock;
  @MockBean SportCategoryPublicService sportCategoryService;
  @MockBean ModularContentPublicService modularContentService;
  @MockBean SeoPagePublicService seoPageService;
  @MockBean FooterMenuService footerMenuService;
  @MockBean SportPublicService sportService;
  @MockBean InitSignpostingPublicService initSignpostingService;
  @MockBean StructurePublicService structureService;
  @MockBean NavigationPointService navigationPointService;
  @MockBean ExtraNavigationPointPublicService extraNavigationPointPublicService;
  @MockBean BuildYourBetPublicService buildYourBetPublicService;
  @MockBean BybTabAvailabilityService bybTabAvailabilityService;
  @MockBean ConnectMenuPublicService connectMenuPublicService;
  @MockBean HeaderContactMenuPublicService headerContactMenuService;
  @MockBean OddsBoostConfigurationService oddsBoostConfigurationService;
  @MockBean QuizPopupSettingPublicService quizPopupService;
  @MockBean TimelineConfigPublicService timelineConfigService;
  @MockBean private BrandService brandService;
  @MockBean VirtualSportPublicService virtualSportPublicService;
  @MockBean private SvgImagePublicService svgImagePublicService;
  @MockBean SeoAutoPagePublicService seoAutoPageService;
  @MockBean SegmentService egmentService;
  @MockBean LuckyDipV2ConfigService luckyDipV2ConfigService;

  @Before
  public void setup() {
    given(brandService.findByBrandCode(anyString())).willReturn(Optional.of(new Brand()));

    given(connectMenuPublicService.findByBrand(anyString()))
        .willReturn(Collections.singletonList(createConnectMenu()));

    given(structureService.getInitialDataConfiguration(anyString()))
        .willReturn(createSystemConfig().getStructure());

    given(headerContactMenuService.find(anyString()))
        .willReturn(Collections.singletonList(createHeaderContactMenu()));

    given(oddsBoostConfigurationService.getPublicDTO(anyString()))
        .willReturn(new OddsBoostConfigDTO());

    given(quizPopupService.findGeneralSettingsByBrand(anyString()))
        .willReturn(Optional.of(new QuizPopupSettingDto()));

    given(timelineConfigService.findGeneralConfigByBrand(anyString()))
        .willReturn(Optional.of(new TimelineGeneralConfigDto()));

    given(svgImagePublicService.getSvgSprite(anyString(), eq(INITIAL.getSpriteName())))
        .willReturn(new SvgSpriteDto(INITIAL.getSpriteName(), "<svg/>"));

    given(timelineConfigService.findGeneralConfigByBrand("bma"))
        .willReturn(Optional.of(new TimelineGeneralConfigDto()));
  }

  @Test
  public void testContentBma() throws Exception {
    mockMvc
        .perform(get(CMS_API + "/bma/initial-data/mobile"))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(containsString("testConnectLinkTitle")))
        .andExpect(content().string(containsString("connectMenu")))
        .andExpect(content().string(containsString("quizPopupSetting")))
        .andExpect(content().string(not(containsString("testHeaderContactLinkTitle"))));
  }

  @Test
  public void testContentLadbrokes() throws Exception {
    mockMvc
        .perform(get(CMS_API + "/ladbrokes/initial-data/mobile"))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(containsString("connectMenu")))
        .andExpect(content().string(containsString("testConnectLinkTitle")))
        .andExpect(content().string(containsString("quizPopupSetting")))
        .andExpect(content().string(not(containsString("testHeaderContactLinkTitle"))));
  }

  @Test
  public void testSegmentedContentLadbrokes() throws Exception {
    mockMvc
        .perform(
            get(
                CMS_API
                    + "/ladbrokes/initial-data/segment/"
                    + SegmentConstants.UNIVERSAL
                    + "/mobile"))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(containsString("connectMenu")))
        .andExpect(content().string(containsString("testConnectLinkTitle")))
        .andExpect(content().string(containsString("quizPopupSetting")))
        .andExpect(content().string(not(containsString("testHeaderContactLinkTitle"))));
  }

  @Test
  public void testSegmentedContentFooterMenuLadbrokes() throws Exception {

    Mockito.when(
            footerMenuService.findAllByBrandAndDeviceType(
                "ladbrokes", "mobile", SegmentConstants.UNIVERSAL))
        .thenReturn(
            new ArrayList<>(
                Arrays.asList(
                    FooterMenuServiceTest.createFooterMenu(
                        "1", true, SegmentConstants.UNIVERSAL))));
    mockMvc
        .perform(
            get(
                CMS_API
                    + "/ladbrokes/initial-data/segment/"
                    + SegmentConstants.UNIVERSAL
                    + "/mobile"))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(containsString("connectMenu")))
        .andExpect(content().string(containsString("testConnectLinkTitle")))
        .andExpect(content().string(containsString("quizPopupSetting")))
        .andExpect(content().string(not(containsString("testHeaderContactLinkTitle"))))
        .andExpect(content().string(containsString("footerMenu")));
  }

  public ConnectMenuDto createConnectMenu() {
    ConnectMenuDto menu = new ConnectMenuDto();
    menu.setLinkTitle("testConnectLinkTitle");
    return menu;
  }

  public StructureDto createSystemConfig() {
    StructureDto structure = new StructureDto();
    structure.setBrand("bma");
    structure.setStructure(Collections.singletonMap("1", Collections.singletonMap("2", true)));
    return structure;
  }

  public HeaderContactMenuDto createHeaderContactMenu() {
    HeaderContactMenuDto menu = new HeaderContactMenuDto();
    menu.setLinkTitle("testHeaderContactLinkTitle");
    return menu;
  }
}
