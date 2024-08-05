package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import java.time.Instant;
import java.util.List;
import java.util.Optional;
import org.bson.types.ObjectId;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.repository.Query;

public interface PromotionRepository extends CustomMongoRepository<Promotion> {

  @Query("{" + "'brand': ?0, " + "'disabled': false," + "'validityPeriodEnd': {'$gt': ?1}" + "}")
  List<Promotion> findPromotions(String brand, Instant now, Sort sorting);

  Optional<Promotion> findPromotionByBrandAndPromotionId(String brand, String promotionId);

  @Query(
      "{"
          + "'brand': ?0, "
          + "'disabled': false,"
          + "'validityPeriodEnd': {'$gt': ?1},"
          + "'promotionId': {'$in': ?2}"
          + "}")
  List<Promotion> findPromotionByPromotionIds(
      String brand, Instant date, List<String> promotionIds);

  @Query(
      "{"
          + "'brand': ?0, "
          + "'disabled': false,"
          + "'validityPeriodEnd': {'$gt': ?1},"
          + "'id': {'$in': ?2}"
          + "}")
  List<Promotion> findPromotionsByIds(String brand, Instant date, List<String> ids);

  List<Promotion> findPromotionByPromotionIdNotIn(List<String> promotionIds);

  @Query(
      "{"
          + "'brand': ?0, "
          + "'disabled': false,"
          + "'validityPeriodEnd': {'$gt': ?1},"
          + "'isSignpostingPromotion': true"
          + "}")
  List<Promotion> findSignpostingPromotions(String brand, Instant now, Sort sorting);

  @Query(
      "{"
          + "'brand': ?0, "
          + "'disabled': false,"
          + "'validityPeriodEnd': {'$gt': ?1}, "
          + "'categoryId': {'$in': ?2}"
          + "}")
  List<Promotion> findPromotionsWithCategoryIds(
      String brand, Instant date, Sort sorting, List<ObjectId> ids);

  @Query(
      "{"
          + "'brand': ?0, "
          + "'disabled': false,"
          + "'validityPeriodEnd': {'$gt': ?1}, "
          + "'competitionId': {'$in': [?2]}"
          + "}")
  List<Promotion> findPromotionsWithCompetitionId(
      String brand, Instant date, Sort sorting, String id);

  Optional<Promotion> findPromotionByBrandAndPromoKey(String brand, String promoKey);

  List<Promotion> findAllByNavigationGroupIdIn(List<String> navigationIds);

  List<Promotion> findAllByNavigationGroupIdInAndValidityPeriodEndIsGreaterThanEqual(
      List<String> navigationIds, Instant endDate);

  List<Promotion> findByNavigationGroupIdAndValidityPeriodEndIsGreaterThanEqual(
      String navGroupId, Instant endDate);

  List<Promotion> findAllByBrandAndValidityPeriodEndIsGreaterThanEqualAndNavigationGroupIdNotNull(
      String brand, Instant endDate);
}
