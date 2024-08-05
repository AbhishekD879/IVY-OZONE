package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.RelationType;
import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBet;
import java.math.BigInteger;
import java.time.Instant;
import java.util.List;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.repository.Query;

public interface SurfaceBetRepository extends CustomSegmentRepository<SurfaceBet> {
  List<SurfaceBet> findByBrandOrderBySortOrderAsc(String brand);

  List<SurfaceBet>
      findByBrandAndDisplayFromIsBeforeAndDisplayToIsAfterAndDisabledIsFalseOrderBySortOrderAsc(
          String brand, Instant from, Instant to);

  void deleteAllByBrandAndPageTypeAndPageId(String brand, PageType pageType, String pageId);

  @Query(
      "{$and:[{'brand' : ?0},{'disabled':false},{'edpOn':true},{'displayFrom':{'$lte':?1}},{'displayTo':{'$gte':?2}}]}")
  List<SurfaceBet> findUniversalRecordsByBrandAndActiveTrue(
      String brand, Instant start, Instant end, Sort order);

  @Query(
      "{$and:[{'brand' : ?0}, {$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{references: {$elemMatch: {'relatedTo':?1, 'refId': ?2}}}]}")
  List<SurfaceBet> findUniversalRecordsByBrandAndPageRef(
      String brand, RelationType pageType, String pageId);

  @Query(
      "{$and:[{'brand' : ?0},{references: {$elemMatch: {'relatedTo':?2, 'refId': ?3}}},{segmentReferences: {$elemMatch: {'sortOrder':{$gte:0}, 'segmentName': {$in: ?1}}}},{$or:[{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'inclusionList':{'$in':?1}}]}]}")
  List<SurfaceBet> findAllByBrandAndSegmentNameAndPageRef(
      String brand, List<String> segmentName, RelationType pageType, String pageId);

  @Query(
      "{ $and:["
          + "{ $and:  [  {references: {$elemMatch: {'relatedTo':?3, 'refId': ?4}}},{'brand' : ?0}]},"
          + "{ $and:  [  {'_id': {'$nin':?2}},{references: {$elemMatch: {'relatedTo':?3, 'refId': ?4}}},{'brand' : ?0}]},"
          + "{ $or:   [  "
          + "{ $and:  [   {references: {$elemMatch: {'relatedTo':?3, 'refId': ?4}}},{'inclusionList':{'$in':?1}},{'brand' :  ?0}]},"
          + "{ $and:  [  {references: {$elemMatch: {'relatedTo':?3, 'refId': ?4}}},{'brand' :  ?0},{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'exclusionList' : {'$nin' : ?1}}]}]}"
          + "]"
          + "}")
  List<SurfaceBet> findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
      String brand,
      List<String> segmentName,
      List<String> inclusiveListIds,
      RelationType pageType,
      String pageId);

  @Query(
      "{$and:[{'brand' : ?0},{'disabled':false},{'selectionId' : ?1},{'displayTo':{'$gte':?2}}]}")
  List<SurfaceBet> findBySelectionIdAndBrand(String brand, BigInteger selectionId, Instant instant);

  @Query("{ brand : ?0,'displayFrom':{'$lte':?1},'displayTo':{'$gte':?1} }")
  List<SurfaceBet> findActiveSurfaceBetsByBrand(String brand, Instant now);
}
