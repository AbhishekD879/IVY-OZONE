package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.NavigationGroupDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavItem;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationGroup;
import com.ladbrokescoral.oxygen.cms.api.entity.PromoLeaderboardConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.repository.NavItemRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.PromoLeaderboardRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.PromotionRepository;
import com.ladbrokescoral.oxygen.cms.api.service.NavItemService;
import com.ladbrokescoral.oxygen.cms.api.service.PromoLeaderboardValidationService;
import com.ladbrokescoral.oxygen.cms.api.service.PromotionLeaderboardMsgPublishService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.io.IOException;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.mockito.AdditionalAnswers;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {NavItemController.class, NavItemService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class NavItemControllerTest extends AbstractControllerTest {

  @MockBean private NavItemRepository navItemRepository;
  @MockBean private PromotionRepository promotionRepository;
  @MockBean private PromotionLeaderboardMsgPublishService promotionLeaderboardMsgPublishService;
  @MockBean private PromoLeaderboardRepository promoLeaderboardRepository;
  @MockBean private PromoLeaderboardValidationService promoLeaderboardValidationService;

  private NavigationGroup navigationGroup;
  private NavItem navItem;
  private NavItem navItem2;
  private Promotion promotion;

  public static final String API_BASE_URL = "/v1/api/nav-item";
  public static final String BRAND = "ladbrokes";
  private static final String NAVIGATION_ID = "101";
  private static final String LEADERBOARD_ID = "L1";
  public static final String LEADERBOARD_NAV_TYPE = "Leaderboard";
  public static final String URL_NAV_TYPE = "URL";

  @Before
  public void init() throws IOException {
    navigationGroup =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createNavigationGrp.json", NavigationGroup.class);
    navItem =
        TestUtil.deserializeWithJackson("controller/private_api/createNavItem.json", NavItem.class);
    navItem.setNavType(URL_NAV_TYPE);

    navItem2 =
        TestUtil.deserializeWithJackson("controller/private_api/createNavItem.json", NavItem.class);

    promotion = new Promotion();
    promotion.setPromoKey("Sandbox");
    promotion.setNavigationGroupId("124");

    given(navItemRepository.save(any(NavItem.class))).will(AdditionalAnswers.returnsFirstArg());
    doReturn(Optional.of(navItem)).when(navItemRepository).findById(any(String.class));
  }

  @Test
  public void createNavItemTest() throws Exception {
    given(
            promotionRepository.findAllByNavigationGroupIdInAndValidityPeriodEndIsGreaterThanEqual(
                any(), any()))
        .willReturn(Arrays.asList(promotion));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createNavItemWithSortOrderTest() throws Exception {
    navItem2.setSortOrder((double) -1);
    given(navItemRepository.findAllNavItemByNavigationGroupId(any(), any()))
        .willReturn(Arrays.asList(navItem2));
    given(
            promotionRepository.findAllByNavigationGroupIdInAndValidityPeriodEndIsGreaterThanEqual(
                any(), any()))
        .willReturn(Arrays.asList(promotion));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createNavItemWithLeaderboardTest() throws Exception {
    navItem.setNavType(LEADERBOARD_NAV_TYPE);
    navItem.setLeaderboardId(LEADERBOARD_ID);
    given(
            promotionRepository.findAllByNavigationGroupIdInAndValidityPeriodEndIsGreaterThanEqual(
                any(), any()))
        .willReturn(Arrays.asList(promotion));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createNavItemWhenPromotionNotLinkedTest() throws Exception {
    given(
            promotionRepository.findAllByNavigationGroupIdInAndValidityPeriodEndIsGreaterThanEqual(
                any(), any()))
        .willReturn(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createNavItemWhenExceptionThrownTest() throws Exception {
    navItem.setNavType(LEADERBOARD_NAV_TYPE);
    navItem.setLeaderboardId(LEADERBOARD_ID);
    given(
            promotionRepository.findAllByNavigationGroupIdInAndValidityPeriodEndIsGreaterThanEqual(
                any(), any()))
        .willReturn(Arrays.asList(promotion));
    doThrow(NullPointerException.class)
        .when(promotionLeaderboardMsgPublishService)
        .publishMessage(any(), any(), any());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void createNavItemWithMaxLbrValidationTest() throws Exception {
    given(promoLeaderboardValidationService.isNavItemValidationRequired(any(), any()))
        .willReturn(true);
    given(
            promotionRepository.findAllByNavigationGroupIdInAndValidityPeriodEndIsGreaterThanEqual(
                any(), any()))
        .willReturn(Arrays.asList(promotion));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateNavItemTest() throws Exception {
    navItem2.setNavType(LEADERBOARD_NAV_TYPE);
    navItem2.setLeaderboardId(LEADERBOARD_ID);
    navItem2.setSortOrder((double) -2);
    given(navItemRepository.findAllNavItemByNavigationGroupId(any(), any()))
        .willReturn(Arrays.asList(navItem2));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + NAVIGATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem2)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateNavItemWithNewLeaderboardTest() throws Exception {
    navItem.setNavType(LEADERBOARD_NAV_TYPE);
    navItem.setLeaderboardId(LEADERBOARD_ID);

    navItem2.setNavType(LEADERBOARD_NAV_TYPE);
    navItem2.setLeaderboardId("L2");
    navItem2.setSortOrder((double) -2);

    given(
            promotionRepository.findAllByNavigationGroupIdInAndValidityPeriodEndIsGreaterThanEqual(
                any(), any()))
        .willReturn(Arrays.asList(promotion));

    given(navItemRepository.findAllNavItemByNavigationGroupId(any(), any()))
        .willReturn(Arrays.asList(navItem2));
    given(promoLeaderboardRepository.findAllById(any()))
        .willReturn(Arrays.asList(createPromoLbrConfig()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + NAVIGATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem2)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateNavItemLbrWithUrlTest() throws Exception {
    navItem.setNavType(LEADERBOARD_NAV_TYPE);
    navItem.setLeaderboardId(LEADERBOARD_ID);

    navItem2.setNavType(URL_NAV_TYPE);
    navItem2.setSortOrder((double) -2);

    given(
            promotionRepository.findAllByNavigationGroupIdInAndValidityPeriodEndIsGreaterThanEqual(
                any(), any()))
        .willReturn(Arrays.asList(promotion));

    given(navItemRepository.findAllNavItemByNavigationGroupId(any(), any()))
        .willReturn(Arrays.asList(navItem2));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + NAVIGATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem2)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateNavItemWithNewUrlTest() throws Exception {
    navItem2.setNavType("url2");
    navItem2.setSortOrder((double) -2);

    given(
            promotionRepository.findAllByNavigationGroupIdInAndValidityPeriodEndIsGreaterThanEqual(
                any(), any()))
        .willReturn(Arrays.asList(promotion));

    given(navItemRepository.findAllNavItemByNavigationGroupId(any(), any()))
        .willReturn(Arrays.asList(navItem2));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + NAVIGATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem2)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateNavItemWhenExceptionThrownTest() throws Exception {
    navItem.setNavType(LEADERBOARD_NAV_TYPE);
    navItem.setLeaderboardId(LEADERBOARD_ID);

    navItem2.setNavType(LEADERBOARD_NAV_TYPE);
    navItem2.setLeaderboardId("L2");
    navItem2.setSortOrder((double) -2);

    given(
            promotionRepository.findAllByNavigationGroupIdInAndValidityPeriodEndIsGreaterThanEqual(
                any(), any()))
        .willReturn(Arrays.asList(promotion));

    given(navItemRepository.findAllNavItemByNavigationGroupId(any(), any()))
        .willReturn(Arrays.asList(navItem2));
    doThrow(NullPointerException.class)
        .when(promotionLeaderboardMsgPublishService)
        .publishMessage(any(), any(), any());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + NAVIGATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem2)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void updateNavItemTestAfterChangingSortOrder() throws Exception {
    navItem.setSortOrder(-2.0);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + NAVIGATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateNavItemWithValidationTest() throws Exception {
    navItem2.setNavType(LEADERBOARD_NAV_TYPE);
    navItem2.setLeaderboardId(LEADERBOARD_ID);
    navItem2.setSortOrder((double) -2);
    given(promoLeaderboardValidationService.isNavItemValidationRequired(any(), any()))
        .willReturn(true);
    given(navItemRepository.findAllNavItemByNavigationGroupId(any(), any()))
        .willReturn(Arrays.asList(navItem2));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + NAVIGATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem2)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateNavItemWithValidationAndExistingNavItemNotNullTest() throws Exception {
    navItem.setNavType(LEADERBOARD_NAV_TYPE);
    navItem.setLeaderboardId(LEADERBOARD_ID);

    navItem2.setSortOrder((double) -2);
    given(promoLeaderboardValidationService.isNavItemValidationRequired(any(), any()))
        .willReturn(true);
    given(navItemRepository.findAllNavItemByNavigationGroupId(any(), any()))
        .willReturn(Arrays.asList(navItem2));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + NAVIGATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem2)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateNavItemWithValidationAndUpdatedNavItemNullTest() throws Exception {
    navItem2.setSortOrder((double) -2);
    given(promoLeaderboardValidationService.isNavItemValidationRequired(any(), any()))
        .willReturn(true);
    given(navItemRepository.findAllNavItemByNavigationGroupId(any(), any()))
        .willReturn(Arrays.asList(navItem2));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + NAVIGATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem2)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getNavigationGroupTest() {
    NavItemService navItemService =
        Mockito.spy(
            new NavItemService(
                navItemRepository,
                promotionRepository,
                new ModelMapper(),
                null,
                promoLeaderboardRepository));
    when(promotionRepository.findAllByNavigationGroupIdIn(any()))
        .thenReturn(Arrays.asList(promotion));
    given(navItemRepository.findAllNavItemByNavigationGroupId(any(), any()))
        .willReturn(Arrays.asList(navItem));
    when(promoLeaderboardRepository.findAllByIdIn(any())).thenReturn(new ArrayList<>());
    Optional<NavigationGroupDto> navigationGroupDto =
        navItemService.findNavigationGroup("124", Optional.of(navigationGroup));
    Assertions.assertNotNull(navigationGroupDto);
  }

  @Test
  public void getNavigationGroupWithPromoIdNullTest() {
    NavItemService navItemService =
        Mockito.spy(
            new NavItemService(
                navItemRepository,
                promotionRepository,
                new ModelMapper(),
                null,
                promoLeaderboardRepository));
    when(promotionRepository.findAllByNavigationGroupIdIn(any())).thenReturn(new ArrayList<>());

    navItem.setNavType(LEADERBOARD_NAV_TYPE);
    navItem.setLeaderboardId("Lbr1");
    given(navItemRepository.findAllNavItemByNavigationGroupId(any(), any()))
        .willReturn(Arrays.asList(navItem));

    PromoLeaderboardConfig promoLeaderboardConfig = new PromoLeaderboardConfig();
    promoLeaderboardConfig.setId(navItem.getLeaderboardId());
    promoLeaderboardConfig.setStatus(false);

    when(promoLeaderboardRepository.findAllByIdIn(any()))
        .thenReturn(Arrays.asList(promoLeaderboardConfig));
    Optional<NavigationGroupDto> navigationGroupDto =
        navItemService.findNavigationGroup("124", Optional.of(navigationGroup));
    Assertions.assertNotNull(navigationGroupDto);
  }

  @Test
  public void getNavigationGroupWithLbrTest() {
    NavItemService navItemService =
        Mockito.spy(
            new NavItemService(
                navItemRepository,
                promotionRepository,
                new ModelMapper(),
                null,
                promoLeaderboardRepository));

    navItem2.setNavType(LEADERBOARD_NAV_TYPE);
    navItem2.setLeaderboardId("Lbr1");

    given(navItemRepository.findAllNavItemByNavigationGroupId(any(), any()))
        .willReturn(Arrays.asList(navItem, navItem2));

    PromoLeaderboardConfig promoLeaderboardConfig = new PromoLeaderboardConfig();
    promoLeaderboardConfig.setId(navItem2.getLeaderboardId());
    promoLeaderboardConfig.setStatus(true);

    when(promoLeaderboardRepository.findAllByIdIn(any()))
        .thenReturn(Arrays.asList(promoLeaderboardConfig));

    Optional<NavigationGroupDto> navigationGroupDto =
        navItemService.findNavigationGroup("124", Optional.of(navigationGroup));
    Assertions.assertNotNull(navigationGroupDto);
  }

  @Test
  public void deleteNavItemWithoutLbrTest() throws Exception {
    navItem.setId(NAVIGATION_ID);
    when(promotionRepository.findAllByNavigationGroupIdInAndValidityPeriodEndIsGreaterThanEqual(
            any(), any()))
        .thenReturn(Arrays.asList(promotion));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/" + NAVIGATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteNavItemTest() throws Exception {
    navItem.setId(NAVIGATION_ID);
    navItem.setNavType(LEADERBOARD_NAV_TYPE);
    navItem.setLeaderboardId(LEADERBOARD_ID);
    when(promotionRepository.findAllByNavigationGroupIdInAndValidityPeriodEndIsGreaterThanEqual(
            any(), any()))
        .thenReturn(Arrays.asList(promotion));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/" + NAVIGATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteNavItemWithLeaderboardExceptionTest() throws Exception {
    navItem.setId(NAVIGATION_ID);
    navItem.setNavType(LEADERBOARD_NAV_TYPE);
    navItem.setLeaderboardId(LEADERBOARD_ID);
    when(promotionRepository.findAllByNavigationGroupIdInAndValidityPeriodEndIsGreaterThanEqual(
            any(), any()))
        .thenReturn(Arrays.asList(promotion));
    doThrow(NullPointerException.class)
        .when(promotionLeaderboardMsgPublishService)
        .publishMessage(any(), any(), any());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/" + NAVIGATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(navItem)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void getLeaderboardNavItemsWithLbrTest() {
    NavItemService navItemService =
        Mockito.spy(
            new NavItemService(
                navItemRepository, promotionRepository, new ModelMapper(), null, null));
    navItem.setNavType(LEADERBOARD_NAV_TYPE);
    given(
            navItemRepository.findAllNavItemByNavTypeEqualsIgnoreCaseAndNavigationGroupId(
                any(), any()))
        .willReturn(Arrays.asList(navItem));
    List<NavItem> navItems = navItemService.getLeaderboardNavItems("124");
    Assertions.assertNotNull(navItems);
  }

  @Test
  public void getLeaderboardNavItemsWithoutLbrTest() {
    NavItemService navItemService =
        Mockito.spy(
            new NavItemService(
                navItemRepository, promotionRepository, new ModelMapper(), null, null));
    given(
            navItemRepository.findAllNavItemByNavTypeEqualsIgnoreCaseAndNavigationGroupId(
                any(), any()))
        .willReturn(Arrays.asList(navItem));
    List<NavItem> navItems = navItemService.getLeaderboardNavItems("124");
    Assertions.assertNotNull(navItems);
  }

  @Test
  public void findAllNavItemsByLbIdTest() {
    NavItemService navItemService =
        Mockito.spy(
            new NavItemService(
                navItemRepository, promotionRepository, new ModelMapper(), null, null));
    given(navItemRepository.findAllNavItemByLeaderboardId(any()))
        .willReturn(Arrays.asList(navItem));
    List<NavItem> navItems = navItemService.findAllNavItemsByLbId("LB1");
    Assertions.assertNotNull(navItems);
  }

  @Test
  public void deleteAllNavItemsTest() {
    NavItemService navItemService =
        Mockito.spy(
            new NavItemService(
                navItemRepository, promotionRepository, new ModelMapper(), null, null));
    doNothing().when(navItemRepository).deleteAll(any());
    navItemService.deleteAllNavItems(Arrays.asList(navItem));
    Assertions.assertNotNull(navItemService);
  }

  @Test
  public void testOrder() throws Exception {
    OrderDto order =
        OrderDto.builder()
            .order(Collections.singletonList("5e7d4a3f983019527c82330b"))
            .id("5e7d4a3f983019527c82330b")
            .build();

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL + "/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(order)))
        .andExpect(status().isOk());
  }

  @Test
  public void findAllNavItemTest() {
    NavItemService navItemService =
        Mockito.spy(new NavItemService(navItemRepository, promotionRepository, null, null, null));
    when(navItemRepository.findAllNavItemByBrand(any())).thenReturn(Arrays.asList(navItem));
    List<NavItem> navItemList = navItemService.findAllNavItem(BRAND);
    Assertions.assertNotNull(navItemList);
  }

  @Test
  public void findAllNavItemByBrandWhereLeaderboardIdNotNullTest() {
    NavItemService navItemService =
        Mockito.spy(
            new NavItemService(
                navItemRepository, promotionRepository, new ModelMapper(), null, null));
    when(navItemRepository.findAllByBrandAndLeaderboardIdNotNull(any()))
        .thenReturn(Arrays.asList(navItem));
    List<NavItem> navItemsList = navItemService.findAllNavItemByBrandWhereLbrIdNotNull(BRAND);
    Assertions.assertNotNull(navItemsList);
  }

  @Test
  public void getNavItemWithActiveLbrTest() {
    PromoLeaderboardConfig promoLeaderboardConfig = createPromoLbrConfig();
    promoLeaderboardConfig.setStatus(true);

    NavItemService navItemService =
        Mockito.spy(
            new NavItemService(
                navItemRepository,
                promotionRepository,
                new ModelMapper(),
                null,
                promoLeaderboardRepository));
    when(promoLeaderboardRepository.findAllByIdIn(any()))
        .thenReturn(Arrays.asList(promoLeaderboardConfig));

    List<NavItem> navItems =
        navItemService.getNavItemWithActiveLbr(Collections.singletonList(navItem));
    Assertions.assertNotNull(navItems);
  }

  @Test
  public void getNavItemWithActiveLbrEmptyTest() {
    PromoLeaderboardConfig promoConfig = createPromoLbrConfig();
    promoConfig.setStatus(true);

    navItem.setNavType(LEADERBOARD_NAV_TYPE);
    navItem.setLeaderboardId(LEADERBOARD_ID);

    navItem2.setNavType(LEADERBOARD_NAV_TYPE);
    navItem2.setLeaderboardId("PL1");

    NavItemService navItemService =
        Mockito.spy(
            new NavItemService(
                navItemRepository,
                promotionRepository,
                new ModelMapper(),
                null,
                promoLeaderboardRepository));
    when(promoLeaderboardRepository.findAllByIdIn(any())).thenReturn(Arrays.asList(promoConfig));

    List<NavItem> navItems =
        navItemService.getNavItemWithActiveLbr(Arrays.asList(navItem, navItem2));
    Assertions.assertNotNull(navItems);
  }

  private PromoLeaderboardConfig createPromoLbrConfig() {
    PromoLeaderboardConfig promoLeaderboardConfig = new PromoLeaderboardConfig();
    promoLeaderboardConfig.setId("PL1");
    promoLeaderboardConfig.setFilePath("file.com");
    return promoLeaderboardConfig;
  }
}
