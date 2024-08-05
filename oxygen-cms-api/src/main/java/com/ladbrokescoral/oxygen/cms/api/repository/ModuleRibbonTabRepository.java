package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.ModuleRibbonTab;
import java.util.List;
import java.util.Optional;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.repository.Query;

public interface ModuleRibbonTabRepository extends CustomSegmentRepository<ModuleRibbonTab> {

  List<ModuleRibbonTab> findAllByBrandAndVisibleOrderBySortOrderAsc(String brand, Boolean visible);

  Optional<ModuleRibbonTab> findOneByBrandAndInternalId(String brand, String internalId);

  @Query("{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]}")
  List<ModuleRibbonTab> findAllByUniversalSegment();

  @Query(
      "{$and:[{'brand' : ?0}, {'visible' : ?1},{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]}]}")
  List<ModuleRibbonTab> findAllUniversalByBrandAndVisibleOrderBySortOrderAsc(
      String brand, Boolean visible, Sort sort);

  @Query(
      "{$and:[{'brand' : ?0},{'visible' : ?1},{segmentReferences: {$elemMatch: {'sortOrder':{$gte:0}, 'segmentName': {$in: ?2}}}}]}")
  List<ModuleRibbonTab> findAllByBrandAndSegmentName(
      String brand, boolean visible, List<String> segmentName);

  @Query(
      "{ $and:["
          + "{ $and:  [  {'_id': {'$nin':?2}},{'brand' : ?0},{'visible' : ?3}]},"
          + "{ $or:   [  "
          + "{ $and:  [   {'inclusionList':{'$in':?1}},{'brand' :  ?0},{'visible' : ?3}]},"
          + "{ $and:  [  {'brand' :  ?0},{'visible' : ?3},{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'exclusionList' : {'$nin' : ?1}}]}]}"
          + "]"
          + "}")
  List<ModuleRibbonTab>
      findByBrandAndDeviceTypeAndIsVisableAndApplyUniversalSegmentsAndNotInExclusionListAndInInclusiveList(
          String brand,
          List<String> segmentName,
          List<String> inclusiveListIds,
          boolean visible,
          Sort sortBySortOrderAsc);

  @Query(
      "{$and:[{'brand' : ?0}, {$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true},{ inclusionList: { $exists: true, $not: {$size: 0} } }]}]}")
  List<ModuleRibbonTab> findUniversalRecordAndInclusiveNotNullAndBrand(String brand, Sort order);

  boolean existsByBrandAndDirectiveNameAndBybVisbleTrue(String brand, String buildYourBet);
}
