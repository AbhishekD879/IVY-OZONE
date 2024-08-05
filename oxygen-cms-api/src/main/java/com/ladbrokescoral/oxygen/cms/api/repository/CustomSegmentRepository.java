package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentEntity;
import java.util.List;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.data.repository.NoRepositoryBean;

@NoRepositoryBean
public interface CustomSegmentRepository<T extends SegmentEntity> extends CustomMongoRepository<T> {

  @Query(
      "{$and:[{'brand' : ?0}, {$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]}]}")
  List<T> findUniversalRecordsByBrand(String brand, Sort order);

  @Query(
      "{$and:[{'brand': ?0,'?1': true}, {$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]}]}")
  List<T> findUniversalRecordsByBrandAndDeviceType(String brand, String deviceType, Sort order);

  @Query(
      "{$and:[{'brand' : ?0},{segmentReferences: {$elemMatch: {'sortOrder':{$gte:0}, 'segmentName': {$in: ?1}}}},{$or:[{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'inclusionList':{'$in':?1}}]}]}")
  List<T> findAllByBrandAndSegmentName(String brand, List<String> segmentName);

  @Query(
      "{$and:[{'brand' : ?0},{segmentReferences: {$elemMatch: {'sortOrder':{$gte:0}, 'segmentName': {$in: ?1}}}},{$or:[{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'inclusionList':{'$in':?1}}]},{'?2': true}]}")
  List<T> findAllByBrandAndSegmentNameAndDeviceType(
      String brand, List<String> segmentName, String deviceType);

  @Query(
      "{ $and:["
          + "{ $and:  [  {'_id': {'$nin':?2}},{'brand' : ?0}]},"
          + "{ $or:   [  "
          + "{ $and:  [   {'inclusionList':{'$in':?1}},{'brand' :  ?0}]},"
          + "{ $and:  [  {'brand' :  ?0},{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'exclusionList' : {'$nin' : ?1}}]}]}"
          + "]"
          + "}")
  List<T> findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
      String brand,
      List<String> segmentName,
      List<String> inclusiveListIds,
      Sort sortBySortOrderAsc);

  @Query(
      "{ $and:["
          + "{ $and:  [  {'_id': {'$nin':?2}},{'brand' : ?0},{'?3' : true}]},"
          + "{ $or:   [  "
          + "{ $and:  [   {'inclusionList':{'$in':?1}},{'brand' :  ?0},{'?3' : true}]},"
          + "{ $and:  [  {'brand' :  ?0},{'?3' : true},{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'exclusionList' : {'$nin' : ?1}}]}]}"
          + "]"
          + "}")
  List<T> findByBrandAndDeviceTypeAndApplyUniversalSegmentsAndNotInExclusionListAndInInclusiveList(
      String brand,
      List<String> segmentName,
      List<String> inclusiveListIds,
      String deviceType,
      Sort sortBySortOrderAsc);

  @Query(
      "{$and:[{'brand' : ?0}, {$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'pageId' : ?2},{'pageType': ?1}]}")
  List<T> findUniversalRecordsByBrandAndPageRef(
      String brand, PageType pageType, String pageId, Sort sortBySortOrderAsc);

  @Query(
      "{$and:[{'brand' : ?0},{'pageId' : ?3},{'pageType': ?2},{segmentReferences: {$elemMatch: {'sortOrder':{$gte:0}, 'segmentName': {$in: ?1}}}},{$or:[{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'inclusionList':{'$in':?1}}]}]}")
  List<T> findAllByBrandAndSegmentNameAndPageRef(
      String brand, List<String> segmentName, PageType pageType, String pageId);

  @Query(
      "{ $and:["
          + "{ $and:  [  {'_id': {'$nin':?2}},{'brand' : ?0},{'pageId' : ?4},{'pageType': ?3}]},"
          + "{ $or:   [  "
          + "{ $and:  [   {'inclusionList':{'$in':?1}},{'brand' :  ?0},{'pageId' : ?4},{'pageType': ?3}]},"
          + "{ $and:  [  {'brand' :  ?0},{'pageId' : ?4},{'pageType': ?3},{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'exclusionList' : {'$nin' : ?1}}]}]}"
          + "]"
          + "}")
  List<T> findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
      String brand,
      List<String> segmentName,
      List<String> inclusiveListIds,
      PageType pageType,
      String pageId,
      Sort sortBySortOrderAsc);

  @Query(
      "{ $and:[{'brand' :  ?0},{$or:[{'exclusionList':{'$in':?1}},{'inclusionList':{'$in':?1}}]}]}")
  List<T> findAllBySegmentNameIninclusiveAndExclusive(String brand, List<String> segments);
}
