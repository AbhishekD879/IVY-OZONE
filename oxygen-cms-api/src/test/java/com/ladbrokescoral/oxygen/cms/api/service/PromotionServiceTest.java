package com.ladbrokescoral.oxygen.cms.api.service;

import static junit.framework.TestCase.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.NavItem;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.exception.PromoLeaderboardException;
import com.ladbrokescoral.oxygen.cms.api.repository.PromotionRepository;
import java.io.IOException;
import java.lang.reflect.Method;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import org.assertj.core.api.Assertions;
import org.bson.types.ObjectId;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class PromotionServiceTest extends BDDMockito {

  @Mock private PromotionRepository promotionRepository;

  @Mock private ImageService imageService;

  @Mock private MultipartFile file;

  @Mock private PromotionLeaderboardMsgPublishService msgPublishService;

  @Mock private NavItemService navItemService;

  @InjectMocks private PromotionService promotionService;

  private Promotion promotion;
  private Promotion updatePromotion;
  private NavItem navItem;
  public static final String BRAND = "ladbrokes";
  private static final String NAVIGATION_GROUP_ID = "1";

  @Before
  public void init() throws IOException {
    promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    updatePromotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    promotion.setValidityPeriodStart(Instant.now());
    promotion.setValidityPeriodEnd(Instant.now());

    navItem =
        TestUtil.deserializeWithJackson("controller/private_api/createNavItem.json", NavItem.class);
  }

  @Test
  public void testPrepareModelBeforeSave() {
    promotion.setVipLevelsInput("5,6");
    Promotion prepared = promotionService.prepareModelBeforeSave(promotion);
    assertEquals(2, prepared.getVipLevels().size());
  }

  @Test
  public void testPrepareModelBeforeSave2() {
    promotion.setVipLevelsInput(null);
    Promotion prepared = promotionService.prepareModelBeforeSave(promotion);
    assertEquals("Opt In Joao1-Joao-bma", prepared.getTitleBrand());
  }

  @Test
  public void testFindByPromotionIdsSorted() {
    when(promotionRepository.findPromotionByPromotionIds(any(), any(), any()))
        .thenReturn(Arrays.asList(promotion));

    List<Promotion> result = promotionService.findByPromotionIdsSorted("bma", Arrays.asList("1"));
    assertEquals("124", result.get(0).getPromotionId());
  }

  @Test
  public void testFindAllSorted() {
    List<Promotion> result = promotionService.findAllSorted();
    assertNotNull(result);
  }

  @Test
  public void findAllByBrandSorted() {
    when(promotionRepository.findPromotions(any(), any(), any()))
        .thenReturn(Arrays.asList(promotion));
    List<Promotion> result = promotionService.findAllByBrandSorted(BRAND);
    assertNotNull(result);
  }

  @Test
  public void findByBrandAndPromotionId() {
    Optional<Promotion> result = promotionService.findByBrandAndPromotionId(BRAND, "1");
    assertNotNull(result);
  }

  @Test
  public void findAllExceptPromotionIds() {
    when(promotionRepository.findPromotionByPromotionIdNotIn(any()))
        .thenReturn(Arrays.asList(promotion));
    List<Promotion> result = promotionService.findAllExceptPromotionIds(Arrays.asList("1"));
    assertNotNull(result);
  }

  @Test
  public void findByIds() {
    when(promotionRepository.findPromotionsByIds(any(), any(), any()))
        .thenReturn(Arrays.asList(promotion));
    List<Promotion> result = promotionService.findByIds(BRAND, Arrays.asList("1"));
    assertNotNull(result);
  }

  @Test
  public void findAllByBrandSortedAndCategoryIds() {
    when(promotionRepository.findPromotionsWithCategoryIds(any(), any(), any(), any()))
        .thenReturn(Arrays.asList(promotion));
    List<Promotion> result =
        promotionService.findAllByBrandSortedAndCategoryIds("bma", Arrays.asList(new ObjectId()));
    assertNotNull(result);
  }

  @Test
  public void findAllByBrandSortedAndCompetitionId() {
    List<Promotion> result = promotionService.findAllByBrandSortedAndCompetitionId(BRAND, "123");
    assertNotNull(result);
  }

  @Test
  public void findSignpostingPromotions() {
    when(promotionRepository.findSignpostingPromotions(any(), any(Instant.class), any()))
        .thenReturn(Arrays.asList(promotion));
    List<Promotion> result = promotionService.findSignpostingPromotions(BRAND);
    assertNotNull(result);
  }

  @Test
  public void findByBrandAndPromoKey() {
    when(promotionRepository.findPromotionByBrandAndPromoKey(any(), anyString()))
        .thenReturn(Optional.of(promotion));
    Optional<Promotion> result =
        promotionService.findByBrandAndPromoKey(BRAND, promotion.getPromoKey());
    assertNotNull(result);
  }

  @Test
  public void savePromotionTest() {
    when(promotionRepository.save(any())).thenReturn(promotion);
    promotionService.save(promotion);
    assertNull(promotion.getNavigationGroupId());
  }

  @Test
  public void savePromotionWithLbrTest() {
    promotion.setNavigationGroupId(NAVIGATION_GROUP_ID);
    when(promotionRepository.save(any())).thenReturn(promotion);
    when(navItemService.getLeaderboardNavItems(any())).thenReturn(Arrays.asList(navItem));
    promotionService.save(promotion);
    assertNotNull(promotion);
  }

  @Test
  public void savePromotionWithoutLbrTest() {
    promotion.setNavigationGroupId(NAVIGATION_GROUP_ID);
    when(promotionRepository.save(any())).thenReturn(promotion);
    when(navItemService.getLeaderboardNavItems(any())).thenReturn(new ArrayList<>());
    promotionService.save(promotion);
    assertNotNull(promotion);
  }

  @Test
  public void saveTestWithException() {
    promotion.setNavigationGroupId(NAVIGATION_GROUP_ID);
    when(promotionRepository.save(any())).thenReturn(promotion);
    when(navItemService.getLeaderboardNavItems(any())).thenReturn(Arrays.asList(navItem));
    doThrow(NullPointerException.class).when(msgPublishService).publishMessage(any(), any(), any());
    Assertions.assertThatExceptionOfType(PromoLeaderboardException.class)
        .isThrownBy(() -> promotionService.save(promotion));
    assertNotNull(promotion);
  }

  @Test
  public void savePromotionWhenDeleteCallTest() throws Exception {
    Map<String, String> tempMap = new HashMap<>();
    tempMap.put("1", "Deleted");
    ReflectionTestUtils.setField(promotionService, "promoDeleteMap", tempMap);
    promotion.setId("1");
    promotion.setNavigationGroupId(NAVIGATION_GROUP_ID);
    when(promotionRepository.save(any())).thenReturn(promotion);
    promotionService.save(promotion);
    assertNotNull(promotion);
  }

  @Test
  public void updatePromotionTestHappyPath() {
    updatePromotion.setPromoKey("New Key");
    when(promotionRepository.save(any())).thenReturn(updatePromotion);
    promotionService.update(promotion, updatePromotion);
    assertNotNull(promotion);
  }

  @Test
  public void updatePromotionWithLbrNavGroupTest() {
    updatePromotion.setNavigationGroupId("2");
    when(navItemService.getLeaderboardNavItems(anyString())).thenReturn(Arrays.asList(navItem));
    when(promotionRepository.save(any())).thenReturn(updatePromotion);
    promotionService.update(promotion, updatePromotion);
    assertNotNull(promotion);
  }

  @Test
  public void updatePromotionWithNewNavGroupTest() {
    promotion.setNavigationGroupId(NAVIGATION_GROUP_ID);
    updatePromotion.setNavigationGroupId("2");
    when(promotionRepository.save(any())).thenReturn(updatePromotion);
    NavItem navItem2 = new NavItem();
    navItem2.setBrand(BRAND);
    navItem2.setNavigationGroupId("2");
    navItem2.setNavType("Leaderboard");
    navItem2.setLeaderboardId("L1");
    when(navItemService.getLeaderboardNavItems(anyString())).thenReturn(Arrays.asList(navItem2));
    promotionService.update(promotion, updatePromotion);
    assertNotNull(promotion);
  }

  @Test
  public void updatePromoTestWhenPromoStartDateChanged() {
    promotion.setNavigationGroupId(NAVIGATION_GROUP_ID);

    updatePromotion.setNavigationGroupId(NAVIGATION_GROUP_ID);
    updatePromotion.setValidityPeriodStart(Instant.now().plus(1, ChronoUnit.DAYS));
    updatePromotion.setValidityPeriodEnd(Instant.now());

    when(navItemService.getLeaderboardNavItems(anyString())).thenReturn(Arrays.asList(navItem));
    when(promotionRepository.save(any())).thenReturn(updatePromotion);
    promotionService.update(promotion, updatePromotion);
    assertNotNull(promotion);
  }

  @Test
  public void updatePromoTestWhenPromoEndDateChanged() {
    promotion.setNavigationGroupId(NAVIGATION_GROUP_ID);

    updatePromotion.setNavigationGroupId(NAVIGATION_GROUP_ID);
    updatePromotion.setValidityPeriodStart(Instant.now());
    updatePromotion.setValidityPeriodEnd(Instant.now().plus(1, ChronoUnit.DAYS));

    when(navItemService.getLeaderboardNavItems(anyString())).thenReturn(Arrays.asList(navItem));
    when(promotionRepository.save(any())).thenReturn(updatePromotion);
    promotionService.update(promotion, updatePromotion);
    assertNotNull(promotion);
  }

  @Test
  public void updatePromoTestWhenPromoEndDateChangedAndLbrNotPresent() {
    promotion.setNavigationGroupId(NAVIGATION_GROUP_ID);

    updatePromotion.setNavigationGroupId(NAVIGATION_GROUP_ID);
    updatePromotion.setValidityPeriodStart(Instant.now());
    updatePromotion.setValidityPeriodEnd(Instant.now().plus(1, ChronoUnit.DAYS));

    when(navItemService.getLeaderboardNavItems(anyString())).thenReturn(new ArrayList<>());
    when(promotionRepository.save(any())).thenReturn(updatePromotion);
    promotionService.update(promotion, updatePromotion);
    assertNotNull(promotion);
  }

  @Test
  public void updatePromoTestWhenPromoDateNotChanged() {
    promotion.setNavigationGroupId(NAVIGATION_GROUP_ID);

    updatePromotion.setNavigationGroupId(NAVIGATION_GROUP_ID);
    updatePromotion.setValidityPeriodEnd(Instant.now());
    updatePromotion.setValidityPeriodStart(Instant.now());

    when(promotionRepository.save(any())).thenReturn(updatePromotion);
    promotionService.update(promotion, updatePromotion);
    assertNotNull(promotion);
  }

  @Test
  public void updatePromoWhenNavGrpDelinkedTest() {
    promotion.setNavigationGroupId(NAVIGATION_GROUP_ID);
    when(promotionRepository.save(any())).thenReturn(updatePromotion);
    when(navItemService.getLeaderboardNavItems(anyString())).thenReturn(new ArrayList<>());
    promotionService.update(promotion, updatePromotion);
    assertNotNull(promotion);
  }

  @Test
  public void updatePromoTestWithException() {
    promotion.setNavigationGroupId(NAVIGATION_GROUP_ID);
    when(promotionRepository.save(any())).thenReturn(promotion);
    when(navItemService.getLeaderboardNavItems(any())).thenReturn(Arrays.asList(navItem));
    doThrow(NullPointerException.class).when(msgPublishService).publishMessage(any(), any(), any());
    Assertions.assertThatExceptionOfType(PromoLeaderboardException.class)
        .isThrownBy(() -> promotionService.update(promotion, updatePromotion));
    assertNotNull(promotion);
  }

  @Test
  public void deletePromoTest() {
    promotion.setNavigationGroupId(NAVIGATION_GROUP_ID);
    when(promotionRepository.findById(anyString())).thenReturn(Optional.of(promotion));
    when(navItemService.getLeaderboardNavItems(any())).thenReturn(Arrays.asList(navItem));
    promotionService.delete("345");
    assertNotNull(promotion);
  }

  @Test
  public void deletePromoTestWithException() {
    promotion.setNavigationGroupId(NAVIGATION_GROUP_ID);
    when(promotionRepository.findById(anyString())).thenReturn(Optional.of(promotion));
    when(navItemService.getLeaderboardNavItems(any())).thenReturn(Arrays.asList(navItem));
    doThrow(NullPointerException.class).when(msgPublishService).publishMessage(any(), any(), any());
    Assertions.assertThatExceptionOfType(PromoLeaderboardException.class)
        .isThrownBy(() -> promotionService.delete("345"));
    assertNotNull(promotion);
  }

  @Test
  public void deletePromoWithNoLbrTest() {
    when(promotionRepository.findById(anyString())).thenReturn(Optional.of(promotion));
    promotionService.delete("89");
    assertNotNull(promotion);
  }

  @Test
  public void getDistinctLeaderboardTest() throws Exception {
    Method method =
        PromotionService.class.getDeclaredMethod(
            "getDistinctLeaderboard", List.class, String.class);
    method.setAccessible(true);
    navItem.setNavType("Leaderboard");
    navItem.setLeaderboardId("L1");
    NavItem navItem2 =
        TestUtil.deserializeWithJackson("controller/private_api/createNavItem.json", NavItem.class);
    navItem2.setNavType("Leaderboard");
    navItem2.setLeaderboardId("L2");
    when(navItemService.getLeaderboardNavItems(any()))
        .thenReturn(Collections.singletonList(navItem));
    Object val =
        method.invoke(promotionService, Arrays.asList(navItem, navItem2), NAVIGATION_GROUP_ID);
    assertEquals(Collections.singletonList(navItem2), val);
  }
}
