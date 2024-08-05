package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.AssetManagement;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Gamification;
import com.ladbrokescoral.oxygen.cms.api.entity.Season;
import com.ladbrokescoral.oxygen.cms.api.repository.AssetManagementRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.GamificationRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SeasonRepository;
import com.ladbrokescoral.oxygen.cms.api.service.GamificationService;
import com.ladbrokescoral.oxygen.cms.api.service.SeasonService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SeasonPublicService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({OneTwoFreeSeasonApi.class, SeasonPublicService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
class OneTwoFreeSeasonApiTest extends AbstractControllerTest {

  @MockBean private SeasonService service;
  @MockBean private SeasonRepository seasonRepository;
  @MockBean private GamificationService gamificationService;
  @MockBean private GamificationRepository gamificationRepository;
  @MockBean private AssetManagementRepository assetManagementRepository;

  private Gamification gamification;
  private List<Season> seasonList;
  private Season entity;
  private final String BASEURL = "/cms/api/ladbrokes/one-two-free";

  @BeforeEach
  void setUp() throws Exception {
    entity =
        TestUtil.deserializeWithJackson("controller/private_api/createSeason.json", Season.class);
    entity.setBrand("ladbrokes");
    entity.setId("1");
    seasonList = new ArrayList<>();
    seasonList.add(entity);

    gamification =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createGamification.json", Gamification.class);
  }

  @Test
  void findAllSeasonByBrandTest() throws Exception {
    given(seasonRepository.findByBrand(anyString())).willReturn(seasonList);
    given(service.findByBrand(any())).willReturn(seasonList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(BASEURL + "/season").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  void getActiveSeasonTest() throws Exception {
    given(service.getActiveSeason(any())).willReturn(seasonList);
    given(
            seasonRepository.findByBrandAndDisplayFromIsLessThanEqualAndDisplayToGreaterThanEqual(
                any(), any(), any()))
        .willReturn(seasonList);
    given(gamificationRepository.findBySeasonId(anyString())).willReturn(Optional.of(gamification));
    given(gamificationService.findGamificationBySeasonId(anyString()))
        .willReturn(Optional.of(gamification));
    given(assetManagementRepository.findByIdIn(any())).willReturn(setAssetManagement());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(BASEURL + "/active-season")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  void getActiveSeasonNotPresentTest() throws Exception {
    given(service.getActiveSeason(any())).willReturn(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(BASEURL + "/active-season")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  void getActiveSeasonWhenGamificationNotPresentTest() throws Exception {
    given(service.getActiveSeason(any())).willReturn(seasonList);
    given(
            seasonRepository.findByBrandAndDisplayFromIsLessThanEqualAndDisplayToGreaterThanEqual(
                any(), any(), any()))
        .willReturn(seasonList);
    given(gamificationService.findGamificationBySeasonId(anyString())).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(BASEURL + "/active-season")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  void getCurrentFutureSeasonsTest() throws Exception {
    given(service.getCurrentFutureSeasons(any())).willReturn(seasonList);
    given(seasonRepository.findByBrandAndDisplayFromIsGreaterThanEqual(any(), any()))
        .willReturn(seasonList);

    Optional<Gamification> gamificationOptional = Optional.of(gamification);
    given(gamificationService.findAllGamificationBySeasonId(any()))
        .willReturn(Collections.singletonList(gamificationOptional));
    given(gamificationRepository.findBySeasonIdIn(any()))
        .willReturn(Collections.singletonList(gamificationOptional));
    given(assetManagementRepository.findByIdIn(any())).willReturn(setAssetManagement());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(BASEURL + "/current-future-seasons")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  void getCurrentFutureSeasonsWhenGamificationNotPresentTest() throws Exception {
    given(service.getCurrentFutureSeasons(any())).willReturn(seasonList);
    given(seasonRepository.findByBrandAndDisplayFromIsGreaterThanEqual(any(), any()))
        .willReturn(seasonList);
    given(gamificationService.findAllGamificationBySeasonId(any())).willReturn(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(BASEURL + "/current-future-seasons")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  void testCurrentFutureSeasonDetails() throws Exception {
    entity.setDisplayTo(Instant.now().plusSeconds(1000));
    given(service.getCurrentFutureSeasons(any())).willReturn(seasonList);
    given(
            seasonRepository.findByBrandAndDisplayFromIsLessThanEqualAndDisplayToGreaterThanEqual(
                any(), any(), any()))
        .willReturn(seasonList);
    given(gamificationService.findAllGamificationBySeasonId(any()))
        .willReturn(Arrays.asList(Optional.of(gamification)));
    given(gamificationRepository.findBySeasonIdIn(any()))
        .willReturn(Arrays.asList(Optional.of(gamification)));
    given(seasonRepository.findByBrandAndDisplayFromIsGreaterThanEqual(any(), any()))
        .willReturn(seasonList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(BASEURL + "/current-future-seasons-v2")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testCurrentFutureSeasonDetailsAsEmpty() throws Exception {
    entity.setDisplayTo(Instant.now().minusSeconds(1000));
    given(service.getCurrentFutureSeasons(any())).willReturn(seasonList);
    given(gamificationService.findAllGamificationBySeasonId(any())).willReturn(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(BASEURL + "/current-future-seasons-v2")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private List<AssetManagement> setAssetManagement() {
    AssetManagement assetManagement1 = new AssetManagement();
    assetManagement1.setId("5784d7ee01b346ab3471d09a");
    assetManagement1.setTeamName("Arsenal");
    AssetManagement assetManagement2 = new AssetManagement();
    assetManagement2.setId("5784d7ee01b346ab3471c09b");
    assetManagement2.setTeamName("Newcastle");
    Filename filename = new Filename();
    filename.setSvg("Arsenal.svg");
    assetManagement2.setTeamsImage(filename);
    return Arrays.asList(assetManagement1, assetManagement2);
  }
}
