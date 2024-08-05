package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.NavItem;
import com.ladbrokescoral.oxygen.cms.api.entity.PromoLeaderboardConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.repository.PromoLeaderboardRepository;
import com.ladbrokescoral.oxygen.cms.api.service.NavItemService;
import com.ladbrokescoral.oxygen.cms.api.service.PromoLeaderboardService;
import com.ladbrokescoral.oxygen.cms.api.service.PromotionLeaderboardMsgPublishService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.io.IOException;
import java.util.Arrays;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {PromoLeaderboardController.class, PromoLeaderboardService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class PromoLeaderboardControllerTest extends AbstractControllerTest {

  @MockBean private PromoLeaderboardRepository promoLeaderboardRepository;
  @MockBean private PromotionLeaderboardMsgPublishService msgPublishService;
  @MockBean private NavItemService navItemService;

  private PromoLeaderboardConfig leaderboardConfig;
  private NavItem navItem;

  public static final String API_BASE_URL = "/v1/api/promo-leaderboard";
  public static final String BRAND = "ladbrokes";
  private static final String LEADERBOARD_ID = "101";
  private static final String LEADERBOARD_ID_2 = "102";

  @Before
  public void init() throws IOException {
    leaderboardConfig =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createPromoLeaderboard.json", PromoLeaderboardConfig.class);
    navItem =
        TestUtil.deserializeWithJackson("controller/private_api/createNavItem.json", NavItem.class);
    given(promoLeaderboardRepository.save(any(PromoLeaderboardConfig.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    doReturn(Optional.of(leaderboardConfig))
        .when(promoLeaderboardRepository)
        .findById(any(String.class));
  }

  @Test
  public void createLeaderboardTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(leaderboardConfig)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void putLeaderboardTest() throws Exception {
    leaderboardConfig.setId(LEADERBOARD_ID);
    Promotion promo = new Promotion();
    promo.setId("P1");
    given(navItemService.getAllLinkedPromotionByNavGroupsId(any()))
        .willReturn(Arrays.asList(promo));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + LEADERBOARD_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .param("isFileChanged", String.valueOf(true))
                .content(TestUtil.convertObjectToJsonBytes(leaderboardConfig)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void putLeaderboardTestWhenFileChangedFalse() throws Exception {
    leaderboardConfig.setId(LEADERBOARD_ID);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + LEADERBOARD_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .param("isFileChanged", String.valueOf(false))
                .content(TestUtil.convertObjectToJsonBytes(leaderboardConfig)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void putLeaderboardTestWhenExceptionThrown() throws Exception {
    leaderboardConfig.setId(LEADERBOARD_ID);
    Promotion promo = new Promotion();
    promo.setId("P1");
    given(navItemService.getAllLinkedPromotionByNavGroupsId(any()))
        .willReturn(Arrays.asList(promo));
    doThrow(NullPointerException.class).when(msgPublishService).publishMessage(any(), any(), any());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + LEADERBOARD_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .param("isFileChanged", String.valueOf(true))
                .content(TestUtil.convertObjectToJsonBytes(leaderboardConfig)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void getLeaderboardTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/" + LEADERBOARD_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(leaderboardConfig)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getLeaderboardByBrandTest() throws Exception {
    PromoLeaderboardConfig leaderboardConfig2 =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createPromoLeaderboard.json", PromoLeaderboardConfig.class);
    leaderboardConfig2.setId(LEADERBOARD_ID_2);
    leaderboardConfig2.setStatus(false);

    leaderboardConfig.setId(LEADERBOARD_ID);
    navItem.setLeaderboardId(LEADERBOARD_ID);
    given(promoLeaderboardRepository.findByBrand(anyString()))
        .willReturn(Arrays.asList(leaderboardConfig, leaderboardConfig2));
    given(navItemService.findAllNavItemByBrandWhereLbrIdNotNull(any()))
        .willReturn(Arrays.asList(navItem));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(leaderboardConfig)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void findAllActivePromoLeaderboardTest() throws Exception {
    given(promoLeaderboardRepository.findByBrand(anyString()))
        .willReturn(Arrays.asList(leaderboardConfig));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/active/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(leaderboardConfig)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteLeaderboardTest() throws Exception {
    Promotion promo = new Promotion();
    promo.setId("P1");
    given(navItemService.getAllLinkedPromotionByNavGroupsId(any()))
        .willReturn(Arrays.asList(promo));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/" + LEADERBOARD_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(leaderboardConfig)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteLeaderboardTestWhenDeleteFail() throws Exception {
    doThrow(NullPointerException.class).when(navItemService).deleteAllNavItems(any());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/" + LEADERBOARD_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(leaderboardConfig)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void deleteLeaderboardTestWhenDeleteFail2() throws Exception {
    Promotion promo = new Promotion();
    promo.setId("P1");
    given(navItemService.getAllLinkedPromotionByNavGroupsId(any()))
        .willReturn(Arrays.asList(promo));
    doThrow(NullPointerException.class).when(msgPublishService).publishMessage(any(), any(), any());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/" + LEADERBOARD_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(leaderboardConfig)))
        .andExpect(status().is5xxServerError());
  }
}
