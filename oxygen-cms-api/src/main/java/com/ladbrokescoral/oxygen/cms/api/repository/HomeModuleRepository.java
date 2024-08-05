package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import java.time.Instant;
import java.util.List;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.repository.DeleteQuery;
import org.springframework.data.mongodb.repository.Query;

public interface HomeModuleRepository extends CustomSegmentRepository<HomeModule> {

  @Query(
      "{"
          + "'visibility.displayFrom': {'$lte': ?0}, "
          + "'visibility.displayTo': {'$gte': ?0}, "
          + "'visibility.enabled': true"
          + "}")
  List<HomeModule> findAllActive(Instant now);

  @Query(
      "{"
          + "'visibility.displayFrom': {'$lte': ?0}, "
          + "'visibility.displayTo': {'$gte': ?0}, "
          + "'visibility.enabled': true, "
          + "'eventsSelectionSettings.autoRefresh': true, "
          + "'dataSelection.selectionType': {'$in' : ?1}"
          + "}")
  List<HomeModule> findWithAutoRefreshAndSelectionTypeIn(Instant now, List<String> selectionTypes);

  @Query(
      "{"
          + "'visibility.displayFrom': {'$lte': ?0}, "
          + "'visibility.displayTo': {'$gte': ?0}, "
          + "'visibility.enabled': true, "
          + "'publishToChannels': {'$in' : [?1]}"
          + "}")
  List<HomeModule> findAllActiveAndPublishToChannel(Instant now, String brand, Sort sorting);

  @Query(
      "{'$and': ["
          + "  {'publishToChannels': {'$in' : [?1]}}, "
          + "  { '$or': ["
          + "    {'visibility.displayFrom': {'$gt': ?0}}, "
          + "    {'visibility.displayTo': {'$lte': ?0}}, "
          + "    {'visibility.enabled': false}"
          + "  ]}"
          + "]}")
  List<HomeModule> findAllInactiveAndPublishToChannel(Instant now, String brand, Sort sorting);

  @Query(
      "{$and:[{'visibility.displayFrom': {'$lte': ?0}},{'visibility.displayTo': {'$gte': ?0}},{'visibility.enabled': ?2},{'publishToChannels': {'$in' : [?1]}}, {$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]}]}")
  List<HomeModule> findAllUniversalActiveAndPublishToChannel(
      Instant now, String brand, boolean active, Sort sortByDisplayOrderAsc);

  @Query(
      "{'$and': ["
          + "  {'publishToChannels': {'$in' : [?1]}}, "
          + "  {$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},"
          + "  { '$or': ["
          + "    {'visibility.displayFrom': {'$gt': ?0}}, "
          + "    {'visibility.displayTo': {'$lte': ?0}}, "
          + "    {'visibility.enabled': false},"
          + "  ]}"
          + "]}")
  List<HomeModule> findAllUniversalInActiveAndPublishToChannel(
      Instant now, String brand, boolean active, Sort sortByDisplayOrderAsc);

  @Query(
      "{'$and': ["
          + "  {'publishToChannels': {'$in' : [?1]}}, "
          + "  {'exclusionList' : {'$nin' : ?3}}, "
          + "  {$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true},{'inclusionList':{'$in':?3}}]},"
          + "  { '$or': ["
          + "    {'visibility.displayFrom': {'$gt': ?0}}, "
          + "    {'visibility.displayTo': {'$lte': ?0}}, "
          + "    {'visibility.enabled': false},"
          + "  ]}"
          + "]}")
  List<HomeModule> findAllUniversalAndSegmentInActiveAndPublishToChannel(
      Instant now,
      String brand,
      boolean active,
      List<String> segmentName,
      Sort sortByDisplayOrderAsc);

  @Query(
      "{ '$or': ["
          + "{'visibility.displayFrom': {'$gt': ?0}}, "
          + "{'visibility.displayTo': {'$lte': ?0}}, "
          + "{'visibility.enabled': false}"
          + "]}")
  List<HomeModule> findAllInactive(Instant now);

  void removeHomeModulesByVisibilityDisplayToBefore(Instant now);

  @Query(
      "{'$and': ["
          + "  {'publishToChannels': {'$in' : [?0]}}, "
          + "  {'pageType': {'$eq' : ?1}},"
          + "  {'pageId': {'$eq' : ?2}}"
          + "]}")
  List<HomeModule> findAll(String brand, PageType pageType, String pageId, Sort sort);

  @DeleteQuery(
      "{'$and': ["
          + "  {'publishToChannels': {'$in' : [?0]}}, "
          + "  {'pageType': {'$eq' : ?1}},"
          + "  {'pageId': {'$eq' : ?2}}"
          + "]}")
  void deleteAll(String brand, PageType pageType, String pageId);

  @Query(
      "{$and:[{'visibility.displayFrom': {'$lte': ?0}},{'visibility.displayTo': {'$gte': ?0}},{'visibility.enabled': ?3},{'publishToChannels': {'$in' : [?1]}},{segmentReferences: {$elemMatch: {'sortOrder':{$gte:0}, 'segmentName': {$in: ?2}}}}]}")
  List<HomeModule> findAllPublishToChannelAndSegmentNameAndIsActive(
      Instant now, String brand, List<String> segmentName, boolean active, Sort sorting);

  @Query(
      "{ $and:["
          + "{ $and:  [  {'_id': {'$nin':?3}},{'visibility.displayFrom': {'$lte': ?0}},{'visibility.displayTo': {'$gte': ?0}},{'visibility.enabled': ?4},{'publishToChannels': {'$in' : [?1]}}]},"
          + "{ $or:   [  "
          + "{ $and:  [ {'inclusionList':{'$in':?2}}, {'visibility.displayFrom': {'$lte': ?0}},{'visibility.displayTo': {'$gte': ?0}},{'visibility.enabled': ?4},{'publishToChannels': {'$in' : [?1]}}]},"
          + "{ $and:  [  {'visibility.displayFrom': {'$lte': ?0}},{'visibility.displayTo': {'$gte': ?0}},{'visibility.enabled': ?4},{'publishToChannels': {'$in' : [?1]}}, {$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'exclusionList' : {'$nin' : ?2}}]}]}"
          + "]"
          + "}")
  List<HomeModule>
      findByPublishToChannelAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
          Instant now,
          String brand,
          List<String> segmentName,
          List<String> inclusiveListIds,
          boolean active,
          Sort sortBySortOrderAsc);

  @Query(
      "{'$and': ["
          + "  {'publishToChannels': {'$in' : [?0]}}, "
          + "  {'pageType': {'$eq' : ?1}},"
          + "  {'pageId': {'$eq' : ?2}},"
          + "  {$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]}"
          + "]}")
  List<HomeModule> findAllUniversalByBrandAndPageIdAndPageType(
      String brand, PageType pageType, String pageId, Sort sort);

  @Query(
      "{'$and': ["
          + "  {'publishToChannels': {'$in' : [?0]}}, "
          + "  {'pageType': {'$eq' : ?1}},"
          + "  {'pageId': {'$eq' : ?2}},"
          + "  {segmentReferences: {$elemMatch: {'sortOrder':{$gte:0}, 'segmentName': {$in: ?3}}}}"
          + "]}")
  List<HomeModule> findAllSegmentByBrandAndPageIdAndPageType(
      String brand, PageType pageType, String pageId, String segmentName, Sort sort);

  @Query(
      "{ $and:["
          + "{ $and:  [  {'_id': {'$nin':?2}},{'publishToChannels': {'$in' : [?0]}},{'pageType': {'$eq' : ?3}},{'pageId': {'$eq' : ?4}}]},"
          + "{ $or:   [  "
          + "{ $and:  [  {'publishToChannels': {'$in' : [?0]}},{'pageType': {'$eq' : ?3}},{'pageId': {'$eq' : ?4}}]},"
          + "{ $and:  [  {'inclusionList':{'$in':?1}}]},"
          + "{ $and:  [  {$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]},{'exclusionList' : {'$nin' : ?1}}]}]}"
          + "]"
          + "}")
  List<HomeModule>
      findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveListAndPageIdAndPageType(
          String brand,
          List<String> segmentName,
          List<String> inclusiveListIds,
          PageType pageType,
          String pageId,
          Sort sortBySortOrderAsc);

  @Query(
      "{"
          + "'visibility.displayFrom': {'$lte': ?0}, "
          + "'visibility.displayTo': {'$gte': ?0}, "
          + "'visibility.enabled': true, "
          + "'publishToChannels': {'$in' : [?1]},"
          + "{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]}, "
          + "}")
  List<HomeModule> findAllActiveAndPublishToChannelAndApplyUniversalSegments(
      Instant now, String brand, Sort sorting);

  @Query(
      "{'$and': ["
          + "{'publishToChannels': {'$in' : [?1]}}, "
          + "{$or:[{'applyUniversalSegments':{$exists: false}},{'applyUniversalSegments':true}]}, "
          + "{ '$or': ["
          + "{'visibility.displayFrom': {'$gt': ?0}}, "
          + "{'visibility.displayTo': {'$lte': ?0}}, "
          + "{'visibility.enabled': false}"
          + "]}"
          + "]}")
  List<HomeModule> findAllInactiveAndPublishToChannelAndApplyUniversalSegments(
      Instant now, String brand, Sort sorting);

  @Query(
      "{ $and:[{'publishToChannels': {'$in' : [?0]}},{$or:[{'exclusionList':{'$in':?1}},{'inclusionList':{'$in':?1}}]}]}")
  List<HomeModule> findAllBySegmentNameIninclusiveAndExclusiveAndPulishToChannels(
      String brand, List<String> segments);
}
