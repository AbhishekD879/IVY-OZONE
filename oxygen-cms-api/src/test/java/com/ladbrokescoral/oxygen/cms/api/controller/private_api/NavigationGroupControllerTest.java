package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.NavigationGroupDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavItem;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationGroup;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.repository.NavItemRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.NavigationGroupRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.PromotionRepository;
import com.ladbrokescoral.oxygen.cms.api.service.NavItemService;
import com.ladbrokescoral.oxygen.cms.api.service.NavigationGroupService;
import com.ladbrokescoral.oxygen.cms.api.service.PromotionLeaderboardMsgPublishService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.mockito.AdditionalAnswers;
import org.mockito.Mockito;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {NavigationGroupController.class, NavigationGroupService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class NavigationGroupControllerTest extends AbstractControllerTest {

  @MockBean private NavigationGroupRepository navigationGroupRepository;
  @MockBean private PromotionRepository promotionRepository;
  @MockBean private NavItemRepository navItemRepository;
  @MockBean private NavItemService navItemService;
  @MockBean private PromotionLeaderboardMsgPublishService msgPublishService;

  private NavigationGroup navigationGroup;
  private Promotion promotion;
  private NavigationGroupDto navigationGroupDto;
  private NavItem navItem;

  public static final String API_BASE_URL = "/v1/api/navigation-group";
  public static final String BRAND = "ladbrokes";
  private static final String PROMO_IDS = "PM1,PM2";
  private static final String NAVIGATION_GROUP_ID = "1";
  public static final String LEADERBOARD_NAV_TYPE = "Leaderboard";

  @Before
  public void init() throws IOException {
    navigationGroup =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createNavigationGrp.json", NavigationGroup.class);
    promotion = createPromotion();
    navigationGroupDto = new NavigationGroupDto();
    navigationGroupDto.setId("124");

    navItem =
        TestUtil.deserializeWithJackson("controller/private_api/createNavItem.json", NavItem.class);
    navItem.setNavType(LEADERBOARD_NAV_TYPE);
    navItem.setLeaderboardId("L1");

    given(navigationGroupRepository.save(any(NavigationGroup.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    doReturn(Optional.of(navigationGroup))
        .when(navigationGroupRepository)
        .findById(any(String.class));
  }

  @Test
  public void createNavigationGroupTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navigationGroup)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateNavigationGroupTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + NAVIGATION_GROUP_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navigationGroup)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getAllNavigationGroupTest() throws Exception {
    navigationGroup.setId(NAVIGATION_GROUP_ID);
    when(navigationGroupRepository.findByBrand(anyString()))
        .thenReturn(Arrays.asList(navigationGroup));
    promotion.setId("PM1");
    when(promotionRepository.findAllByNavigationGroupIdIn(Arrays.asList(NAVIGATION_GROUP_ID)))
        .thenReturn(Arrays.asList(promotion));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navigationGroup)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getAllNavigationGroupWithoutPromoIdsTest() throws Exception {
    navigationGroup.setId(NAVIGATION_GROUP_ID);
    when(navigationGroupRepository.findByBrand(anyString()))
        .thenReturn(Arrays.asList(navigationGroup));
    when(promotionRepository.findAllByNavigationGroupIdIn(Arrays.asList(NAVIGATION_GROUP_ID)))
        .thenReturn(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navigationGroup)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getActiveNavigationGroupTest() throws Exception {
    navigationGroup.setId(NAVIGATION_GROUP_ID);
    when(navigationGroupRepository.findByBrand(anyString()))
        .thenReturn(Arrays.asList(navigationGroup));
    promotion.setId("PM1");
    when(promotionRepository.findAllByNavigationGroupIdIn(Arrays.asList(NAVIGATION_GROUP_ID)))
        .thenReturn(Arrays.asList(promotion));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/active/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navigationGroup)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteNavigationGroupTest() throws Exception {
    when(promotionRepository.findAllById(any())).thenReturn(Arrays.asList(new Promotion()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(
                    API_BASE_URL + "/" + NAVIGATION_GROUP_ID + "/" + PROMO_IDS)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navigationGroup)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteNavigationGroupWhenPromotionNotLinkedTest() throws Exception {
    doNothing().when(navigationGroupRepository).deleteById(any());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/" + NAVIGATION_GROUP_ID + "/ ")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navigationGroup)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteNavigationGroupWhenLeaderboardIdsNotEmptyTest() throws Exception {
    when(promotionRepository.findAllById(any())).thenReturn(Arrays.asList(new Promotion()));
    given(navItemService.getLeaderboardNavItems(any())).willReturn(Arrays.asList(navItem));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(
                    API_BASE_URL + "/" + NAVIGATION_GROUP_ID + "/" + PROMO_IDS)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navigationGroup)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteNavigationGroupWhenLeaderboardIdsEmptyTest() throws Exception {
    when(promotionRepository.findAllById(any())).thenReturn(Arrays.asList(new Promotion()));
    given(navItemService.getLeaderboardNavItems(any())).willReturn(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(
                    API_BASE_URL + "/" + NAVIGATION_GROUP_ID + "/" + PROMO_IDS)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navigationGroup)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteNavigationGroupWhenMsgPublishingFailTest() throws Exception {
    when(promotionRepository.findAllById(any())).thenReturn(Arrays.asList(new Promotion()));
    given(navItemService.getLeaderboardNavItems(any())).willReturn(Arrays.asList(navItem));

    doThrow(NullPointerException.class).when(msgPublishService).publishMessage(any(), any(), any());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(
                    API_BASE_URL + "/" + NAVIGATION_GROUP_ID + "/" + PROMO_IDS)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navigationGroup)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void findAllNavigationGroupByBrandTest() {
    NavigationGroupService navigationGroupService =
        Mockito.spy(
            new NavigationGroupService(
                navigationGroupRepository,
                promotionRepository,
                navItemRepository,
                null,
                navItemService,
                null));
    when(navigationGroupRepository.findAllNavigationGroupByBrandAndStatusIsTrue(any()))
        .thenReturn(Arrays.asList(navigationGroup));
    List<NavigationGroup> navigationGroupList =
        navigationGroupService.findAllActiveNavigationGroupByBrand(BRAND);
    Assertions.assertNotNull(navigationGroupList);
  }

  @Test
  public void getNavigationGroupTest() throws Exception {
    given(navItemService.findNavigationGroup(any(), any()))
        .willReturn(Optional.of(navigationGroupDto));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/nav-item/navigation-groupId/124")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navigationGroup)))
        .andExpect(status().is2xxSuccessful());
  }

  private Promotion createPromotion() {
    Promotion promotion = new Promotion();
    promotion.setPromoKey("Sandbox");
    promotion.setNavigationGroupId(NAVIGATION_GROUP_ID);
    return promotion;
  }
}
