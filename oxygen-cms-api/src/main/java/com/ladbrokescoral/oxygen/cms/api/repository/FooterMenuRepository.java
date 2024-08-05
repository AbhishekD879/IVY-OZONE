package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import java.util.List;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.repository.Query;

public interface FooterMenuRepository
    extends CustomSegmentRepository<FooterMenu>, FindByRepository<FooterMenu> {

  @Query(
      "{$and:[{'brand' : ?0},{'disabled': false},{segmentReferences: {$elemMatch: {'sortOrder':{$gte:0}, 'segmentName': {$in: ?1}}}},{$or:[{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'inclusionList':{'$in':?1}}]},{'?2': true}]}")
  List<FooterMenu> findAllByBrandAndSegmentNameAndDeviceType(
      String brand,
      List<String> segmentName,
      String deviceType,
      Sort sortBySegmentReferenceSortAsc);

  @Query(
      "{$and:[{'brand' : ?0},{segmentReferences: {$elemMatch: {'sortOrder':{$gte:0}, 'segmentName': {$in: ?1}}}},{$or:[{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'inclusionList':{'$in':?1}}]}]}")
  List<FooterMenu> findAllByBrandAndSegmentName(
      String brand, List<String> asList, boolean isDisabled);

  @Query(
      "{$and:[{'brand' : ?0},{segmentReferences: {$elemMatch: {'sortOrder':{$gte:0}, 'segmentName': {$in: ?1}}}},{$or:[{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'inclusionList':{'$in':?1}}]},{'?2': true}]}")
  List<FooterMenu> findAllByBrandAndSegmentNameAndDeviceType(
      String brand, List<String> asList, String deviceType, boolean isDisabled);

  @Query(
      "{ $and:["
          + "{ $and:  [ {'disabled': false},{'brand' : ?0}]},"
          + "{ $and:  [  {'_id': {'$nin':?2}},{'brand' : ?0}]},"
          + "{ $or:   [  "
          + "{ $and:  [   {'inclusionList':{'$in':?1}},{'brand' :  ?0}]},"
          + "{ $and:  [  {'brand' :  ?0},{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'exclusionList' : {'$nin' : ?1}}]}]}"
          + "]"
          + "}")
  List<FooterMenu> findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
      String brand,
      List<String> segmentName,
      List<String> inclusiveListIds,
      boolean isDisable,
      Sort sortBySortOrderAsc);

  @Query(
      "{ $and:["
          + "{ $and:  [ {'disabled': false},{'brand' : ?0}]},"
          + "    { $and:  [  {'_id': {'$nin':?2}},{'brand' : ?0},{'?3' : true}]},"
          + "{ $or:   [  "
          + "{ $and:  [   {'inclusionList':{'$in':?1}},{'brand' :  ?0},{'?3' : true}]},"
          + "{ $and:  [  {'brand' :  ?0},{'?3' : true},{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'exclusionList' : {'$nin' : ?1}}]}]}"
          + "]"
          + "}")
  List<FooterMenu>
      findByBrandAndDeviceTypeAndApplyUniversalSegmentsAndNotInExclusionListAndInInclusiveList(
          String brand,
          List<String> segmentName,
          List<String> inclusiveListIds,
          String deviceType,
          boolean isDisable,
          Sort sortBySortOrderAsc);

  @Query(
      "{$and:[{'brand' : ?0},{'disabled': false}, {$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]}]}")
  List<FooterMenu> findUniversalRecordsByBrand(
      String brand, boolean isDisable, PageRequest pageRequest);

  @Query(
      "{$and:[{'brand': ?0, 'disabled': false, '?1': true}, {$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]}]}")
  List<FooterMenu> findUniversalRecordsByBrand(
      String brand, String value, boolean isDisable, PageRequest pageRequest);

  @Query("{'brand' : ?0, 'disabled': false}")
  List<FooterMenu> findAllActiveRecordsByBrand(String brand, PageRequest pageRequest);
}
