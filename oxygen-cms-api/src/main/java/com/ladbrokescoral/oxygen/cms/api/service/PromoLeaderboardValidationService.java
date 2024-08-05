package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.exception.PromoLeaderboardException;
import com.ladbrokescoral.oxygen.cms.api.repository.NavItemRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.PromotionRepository;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class PromoLeaderboardValidationService {

  private final NavItemRepository navItemRepository;

  private final PromotionRepository promotionRepository;

  @Value(value = "${promoleaderboard.max.count}")
  private long maxCount;

  public static final String LEADERBOARD_NAV_TYPE = "Leaderboard";

  public PromoLeaderboardValidationService(
      NavItemRepository navItemRepository, PromotionRepository promotionRepository) {
    this.navItemRepository = navItemRepository;
    this.promotionRepository = promotionRepository;
  }

  public void validateMaxLeaderboard(
      String brand, long newlyAddedLbrCount, List<String> excludePromoList) {
    List<Promotion> promotions =
        promotionRepository
            .findAllByBrandAndValidityPeriodEndIsGreaterThanEqualAndNavigationGroupIdNotNull(
                brand, Instant.now());
    Map<String, Set<String>> navGroupPromotionMap =
        promotions.stream()
            .filter(
                p -> !p.getNavigationGroupId().isEmpty() && !excludePromoList.contains(p.getId()))
            .collect(
                Collectors.groupingBy(
                    Promotion::getNavigationGroupId,
                    Collectors.mapping(Promotion::getId, Collectors.toSet())));
    List<NavItem> navItems =
        navItemRepository.findAllByBrandAndNavTypeEqualsIgnoreCaseAndNavigationGroupIdIn(
            brand, LEADERBOARD_NAV_TYPE, navGroupPromotionMap.keySet());
    Map<String, List<String>> navGroupLbMap =
        navItems.stream()
            .filter(
                navItem ->
                    Objects.nonNull(navItem.getLeaderboardId())
                        && !navItem.getLeaderboardId().isEmpty())
            .collect(
                Collectors.groupingBy(
                    NavItem::getNavigationGroupId,
                    Collectors.mapping(NavItem::getLeaderboardId, Collectors.toList())));
    long leaderboardCount = 0;
    for (Map.Entry<String, List<String>> navGroupLbEntry : navGroupLbMap.entrySet()) {
      long lbCount = navGroupLbEntry.getValue().size();
      long promoCount = navGroupPromotionMap.get(navGroupLbEntry.getKey()).size();
      leaderboardCount = leaderboardCount + lbCount * promoCount;
    }
    if ((leaderboardCount + newlyAddedLbrCount) > maxCount) {
      log.error(
          "Error occurred, More than {} leaderboard configuration are not allowed ", maxCount);
      throw new PromoLeaderboardException(
          "More than " + maxCount + " leaderboards are not allowed");
    }
  }

  public boolean isPromotionLinkedWithNavGroup(String navGroupId) {
    return !promotionRepository
        .findByNavigationGroupIdAndValidityPeriodEndIsGreaterThanEqual(navGroupId, Instant.now())
        .isEmpty();
  }

  public long getLinkedPromotionsCount(String navGroupId) {
    return promotionRepository
        .findByNavigationGroupIdAndValidityPeriodEndIsGreaterThanEqual(navGroupId, Instant.now())
        .size();
  }

  public boolean isNavItemValidationRequired(String navType, String navGroupId) {
    return LEADERBOARD_NAV_TYPE.equalsIgnoreCase(navType)
        && isPromotionLinkedWithNavGroup(navGroupId);
  }

  public long getNavGrpLbrCount(String navGroupId) {
    return navItemRepository
        .findAllNavItemByNavTypeEqualsIgnoreCaseAndNavigationGroupId(
            LEADERBOARD_NAV_TYPE, navGroupId)
        .size();
  }
}
