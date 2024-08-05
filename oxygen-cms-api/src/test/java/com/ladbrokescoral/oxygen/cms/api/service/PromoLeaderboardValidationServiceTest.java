package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.NavItem;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.exception.PromoLeaderboardException;
import com.ladbrokescoral.oxygen.cms.api.repository.NavItemRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.PromotionRepository;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.assertj.core.api.Assertions;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class PromoLeaderboardValidationServiceTest extends BDDMockito {

  @Mock private NavItemRepository navItemRepository;

  @Mock private PromotionRepository promotionRepository;

  @InjectMocks private PromoLeaderboardValidationService promoLeaderboardValidationService;

  public static final String BRAND = "ladbrokes";

  public static final String NAVIGATION_ID = "NG1";
  public static final String LEADERBOARD_NAV_TYPE = "Leaderboard";
  private Promotion promotion;
  private NavItem navItem;

  @Before
  public void setUp() throws Exception {
    promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    navItem =
        TestUtil.deserializeWithJackson("controller/private_api/createNavItem.json", NavItem.class);
  }

  @Test
  public void validateMaxLeaderboardTest() throws Exception {
    Field maxCountLimit = PromoLeaderboardValidationService.class.getDeclaredField("maxCount");
    maxCountLimit.setAccessible(true);
    maxCountLimit.set(promoLeaderboardValidationService, 20);

    promotion.setNavigationGroupId(NAVIGATION_ID);
    navItem.setNavigationGroupId(NAVIGATION_ID);
    navItem.setNavType(LEADERBOARD_NAV_TYPE);
    navItem.setLeaderboardId("L1");
    given(
            promotionRepository
                .findAllByBrandAndValidityPeriodEndIsGreaterThanEqualAndNavigationGroupIdNotNull(
                    any(), any()))
        .willReturn(Arrays.asList(promotion));
    given(
            navItemRepository.findAllByBrandAndNavTypeEqualsIgnoreCaseAndNavigationGroupIdIn(
                any(), any(), any()))
        .willReturn(Arrays.asList(navItem));
    promoLeaderboardValidationService.validateMaxLeaderboard(BRAND, 0, new ArrayList<>());
    Assert.assertEquals(NAVIGATION_ID, promotion.getNavigationGroupId());
  }

  @Test
  public void validateMaxLeaderboardTestWhenNavGIdEmptyAndLbIdNull() {
    promotion.setNavigationGroupId("");
    navItem.setNavigationGroupId(NAVIGATION_ID);
    given(
            promotionRepository
                .findAllByBrandAndValidityPeriodEndIsGreaterThanEqualAndNavigationGroupIdNotNull(
                    any(), any()))
        .willReturn(Arrays.asList(promotion));
    given(
            navItemRepository.findAllByBrandAndNavTypeEqualsIgnoreCaseAndNavigationGroupIdIn(
                any(), any(), any()))
        .willReturn(Arrays.asList(navItem));
    promoLeaderboardValidationService.validateMaxLeaderboard(
        BRAND, 0, Arrays.asList(promotion.getId()));
    Assert.assertEquals(NAVIGATION_ID, navItem.getNavigationGroupId());
  }

  @Test
  public void validateMaxLeaderboardTestWhenUpdateExistingNavGroup() {
    promotion.setNavigationGroupId(NAVIGATION_ID);
    navItem.setNavigationGroupId(NAVIGATION_ID);
    navItem.setLeaderboardId("");
    given(
            promotionRepository
                .findAllByBrandAndValidityPeriodEndIsGreaterThanEqualAndNavigationGroupIdNotNull(
                    any(), any()))
        .willReturn(Arrays.asList(promotion));
    given(
            navItemRepository.findAllByBrandAndNavTypeEqualsIgnoreCaseAndNavigationGroupIdIn(
                any(), any(), any()))
        .willReturn(Arrays.asList(navItem));
    promoLeaderboardValidationService.validateMaxLeaderboard(
        BRAND, 0, Arrays.asList(promotion.getId()));
    Assert.assertEquals(NAVIGATION_ID, promotion.getNavigationGroupId());
  }

  @Test
  public void validateMaxLeaderboardTestWithException() {
    List<String> excludePromoList = Arrays.asList(promotion.getId());
    Assertions.assertThatExceptionOfType(PromoLeaderboardException.class)
        .isThrownBy(
            () ->
                promoLeaderboardValidationService.validateMaxLeaderboard(
                    BRAND, 1, excludePromoList));
  }

  @Test
  public void isNavItemValidationRequiredTest() {
    given(
            promotionRepository.findByNavigationGroupIdAndValidityPeriodEndIsGreaterThanEqual(
                any(), any()))
        .willReturn(Arrays.asList(promotion));
    boolean res =
        promoLeaderboardValidationService.isNavItemValidationRequired(
            LEADERBOARD_NAV_TYPE, NAVIGATION_ID);
    Assert.assertTrue(res);
  }

  @Test
  public void isNavItemValidationRequiredTestFalse() {
    given(
            promotionRepository.findByNavigationGroupIdAndValidityPeriodEndIsGreaterThanEqual(
                any(), any()))
        .willReturn(new ArrayList<>());
    boolean res =
        promoLeaderboardValidationService.isNavItemValidationRequired(
            LEADERBOARD_NAV_TYPE, NAVIGATION_ID);
    Assert.assertFalse(res);
  }

  @Test
  public void isNavItemValidationRequiredTestWhenNavTypeUrl() {
    boolean res =
        promoLeaderboardValidationService.isNavItemValidationRequired("url", NAVIGATION_ID);
    Assert.assertFalse(res);
  }

  @Test
  public void getLinkedPromotionsCountTest() {
    given(
            promotionRepository.findByNavigationGroupIdAndValidityPeriodEndIsGreaterThanEqual(
                any(), any()))
        .willReturn(Arrays.asList(promotion));
    long res = promoLeaderboardValidationService.getLinkedPromotionsCount(NAVIGATION_ID);
    Assert.assertEquals(1L, res);
  }

  @Test
  public void getNavGrpLbrCountTest() {
    given(
            navItemRepository.findAllNavItemByNavTypeEqualsIgnoreCaseAndNavigationGroupId(
                any(), any()))
        .willReturn(Arrays.asList(navItem));
    long res = promoLeaderboardValidationService.getNavGrpLbrCount(NAVIGATION_ID);
    Assert.assertEquals(1L, res);
  }
}
