package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Relation;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.function.Function;
import java.util.function.ToDoubleFunction;
import java.util.stream.Collectors;
import org.bson.types.ObjectId;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;

public interface SegmentedService<T extends SegmentEntity> extends SegmentedSortService<T> {

  public abstract List<T> getAllRecordsBySegmentName(
      String brand, String segmentName, Optional<String> deviceType);

  public abstract List<T> findAllUniversalAndNotInsegmentReferences(
      String brand, String segmentName, List<String> inclusiveListIds, Optional<String> deviceType);

  public abstract List<T> getUniversal(String brand, Optional<String> deviceType);

  public abstract void createSegments(List<String> segments, String brand);

  public abstract <E extends T> void saveArchivalEntity(E archivalEntity);

  public abstract <S extends T> S saveEntity(S entity);

  public abstract <S extends T> S prepareArchivalEntity(T entity);

  public void saveAndUpdateArchivals(Iterable<T> list);

  default List<T> findByBrandAndSegmentName(String brand, String segmentName) {

    List<T> records =
        SegmentConstants.UNIVERSAL.equalsIgnoreCase(segmentName)
            ? getUniversal(brand, Optional.empty())
            : getSegmentAndUniversal(brand, segmentName, Optional.empty());

    return records.stream().map(this::enhanceEntity).collect(Collectors.toList());
  }

  /** Method to return all the records BY Brand and SegmentName and universal */
  default List<T> getSegmentAndUniversal(
      String brand, String segmentName, Optional<String> deviceType) {
    List<T> recordsWithSegmentReference =
        getAllrecordsWithSegmentReferenceBySortOrder(brand, segmentName, deviceType);
    /* Add text if universal segment touched... */
    isUniversalSegmentChanged(recordsWithSegmentReference, segmentName);
    List<String> inclusiveListIds =
        recordsWithSegmentReference.stream().map(T::getId).collect(Collectors.toList());
    List<T> universalList =
        findAllUniversalAndNotInsegmentReferences(brand, segmentName, inclusiveListIds, deviceType);
    recordsWithSegmentReference.addAll(universalList);

    return recordsWithSegmentReference;
  }

  default List<T> getAllrecordsWithSegmentReferenceBySortOrder(
      String brand, String segmentName, Optional<String> deviceType) {
    List<T> recordsWithSegmentReference =
        getAllRecordsBySegmentName(brand, segmentName, deviceType);

    return sortByOrder(segmentName, recordsWithSegmentReference);
  }

  /** sort the records based on segment level sort order */
  default List<T> sortByOrder(String segmentName, List<T> recordsWithSegmentReference) {

    if (CollectionUtils.isEmpty(recordsWithSegmentReference)) return new ArrayList<>();

    Map<String, T> mapRecords =
        recordsWithSegmentReference.stream()
            .collect(Collectors.toMap(T::getId, Function.identity()));

    ToDoubleFunction<T> sortOrder =
        entity ->
            entity
                .getSegmentReferences()
                .parallelStream()
                .filter(references -> segmentName.equals(references.getSegmentName()))
                .findFirst()
                .get()
                .getSortOrder();

    Map<String, Double> mapSortOrder =
        recordsWithSegmentReference.stream()
            .collect(Collectors.toMap(T::getId, sortOrder::applyAsDouble))
            .entrySet()
            .stream()
            .sorted(Map.Entry.comparingByValue())
            .collect(
                Collectors.toMap(
                    Map.Entry::getKey, Map.Entry::getValue, (e1, e2) -> e1, LinkedHashMap::new));

    return mapSortOrder.keySet().stream().map(mapRecords::get).collect(Collectors.toList());
  }

  public default void updateSegmentReferencesAndPageReference(
      T entity, Optional<Relation> relation) {

    // case 1 if relation is empty then this record is not the segmented.so it should be universal
    // no segment reference are available until it is sorted

    // case 2 :if it is universal record then only then only exclusivelist segmentents to be be
    // removed and defaylt universal segment to be added

    // case3  :if the record is Segmented then except inclusive segments all other to be removed
    // from the SegmentReferences including universal
    if (!relation.isPresent()) {
      entity.setSegmentReferences(new ArrayList<>());
    } else if (entity.isUniversalSegment()) {
      computeUniversalSegmentReferences(entity, relation);
    } else {

      entity.setSegmentReferences(
          buildDefaultSegmentList(
              relation.get().getId(),
              new HashSet<>(entity.getInclusionList()),
              entity.getSegmentReferences()));
    }
  }

  public default void computeUniversalSegmentReferences(T entity, Optional<Relation> relation) {
    if (relation.isPresent()) {
      if (CollectionUtils.isEmpty(entity.getSegmentReferences())) {
        entity.setSegmentReferences(buildDefaultUniversalList(relation.get().getId()));
      } else {

        List<SegmentReference> references = entity.getSegmentReferences();
        entity.setSegmentReferences(isUniversalSegmentPresent(references, relation.get().getId()));

        if (!CollectionUtils.isEmpty(entity.getExclusionList())) {
          entity.setSegmentReferences(
              entity.getSegmentReferences().stream()
                  .filter(
                      reference -> !entity.getExclusionList().contains(reference.getSegmentName()))
                  .collect(Collectors.toList()));
        }
      }
    }
  }

  public default List<SegmentReference> isUniversalSegmentPresent(
      List<SegmentReference> references, String pageId) {

    boolean isexsists =
        references.stream()
            .anyMatch(ref -> SegmentConstants.UNIVERSAL.equals(ref.getSegmentName()));

    if (!isexsists) {
      references.add(buildDefaultSegmentReference(SegmentConstants.UNIVERSAL, pageId));
    }
    return references;
  }

  public default List<SegmentReference> buildDefaultUniversalList(String pageId) {
    List<SegmentReference> references = new ArrayList<>();
    references.add(buildDefaultSegmentReference(SegmentConstants.UNIVERSAL, pageId));
    return references;
  }

  public default List<SegmentReference> buildDefaultSegmentList(
      String pageId, Set<String> inclusiveSegmentNames, List<SegmentReference> existingReferences) {

    if (CollectionUtils.isEmpty(existingReferences)) {
      inclusiveSegmentNames.forEach(
          (String segment) ->
              existingReferences.add(buildDefaultSegmentReference(segment, pageId)));

    } else {

      addNewSegmentReferenceForInclusiveList(existingReferences, inclusiveSegmentNames, pageId);
    }

    return existingReferences;
  }

  public default void addNewSegmentReferenceForInclusiveList(
      List<SegmentReference> segmentReferences, Set<String> inclusionList, String pageRef) {

    Set<String> existingSegmentNames = new HashSet<>();
    existingSegmentNames.addAll(extractSegmentNames(segmentReferences));

    segmentReferences.addAll(
        inclusionList.stream()
            .filter(segmentName -> !existingSegmentNames.contains(segmentName))
            .map(segmentName -> buildDefaultSegmentReference(segmentName, pageRef))
            .collect(Collectors.toList()));

    Iterator<SegmentReference> referenceIterator = segmentReferences.iterator();

    while (referenceIterator.hasNext()) {
      String segmentName = referenceIterator.next().getSegmentName();
      if (SegmentConstants.UNIVERSAL.equals(segmentName) || !inclusionList.contains(segmentName)) {
        referenceIterator.remove();
      }
    }
  }

  public default void updateSegmentReferences(T entity) {

    entity.setSegmentReferences(
        entity.isUniversalSegment()
            ? removeSegmentReferenceForInExclusiveList(
                entity.getSegmentReferences(), new HashSet<>(entity.getExclusionList()))
            : removeSegmentReferenceForNotInInclusiveList(
                entity.getSegmentReferences(), new HashSet<>(entity.getInclusionList())));
    if (entity.isUniversalSegment()) entity.setInclusionList(new ArrayList<>());
  }

  /** removing the Segment references for the record which are in Exclusive List */
  default List<SegmentReference> removeSegmentReferenceForInExclusiveList(
      List<SegmentReference> segmentReferences, Set<String> exclusionList) {
    return segmentReferences.stream()
        .filter(x -> !exclusionList.contains(x.getSegmentName()))
        .collect(Collectors.toList());
  }

  /**
   * compare segment references and inclusive list and remove references not exists in inclusive
   * list
   */
  default List<SegmentReference> removeSegmentReferenceForNotInInclusiveList(
      List<SegmentReference> segmentReferences, Set<String> inclusionList) {

    List<String> inSegmentReferences =
        segmentReferences.stream()
            .map(SegmentReference::getSegmentName)
            .collect(Collectors.toList());

    inclusionList.stream()
        .filter(x -> !inSegmentReferences.contains(x))
        .collect(Collectors.toList())
        .forEach(x -> segmentReferences.add(buildDefaultSegmentReference(x)));

    return segmentReferences.stream()
        .filter(x -> inclusionList.contains(x.getSegmentName()))
        .collect(Collectors.toList());
  }

  default SegmentReference buildDefaultSegmentReference(String segmentName, String id) {

    return buildSegmentReference(segmentName, DEFAULT_SORT_ORDER_STEP, id);
  }

  default SegmentReference buildDefaultSegmentReference(String segmentName) {

    return buildSegmentReference(segmentName, DEFAULT_SORT_ORDER_STEP);
  }

  default <S extends T> S enhanceArchivalEntity(T archival) {
    archival.setId(null);
    return (S) archival;
  }

  default <S extends T> S save(S entity) {
    if (!StringUtils.hasText(entity.getArchivalId()))
      entity.setArchivalId(ObjectId.get().toHexString());
    updateSegmentReferences(entity);
    entity = saveEntity(entity);
    updateSegments(entity);
    prepareAndSaveArchivalEntity(entity);

    return entity;
  }

  default void updateSegments(T entity) {
    List<String> segments =
        entity.isUniversalSegment() ? entity.getExclusionList() : entity.getInclusionList();
    createSegments(segments, entity.getBrand());
  }

  default <S extends T> void prepareAndSaveArchivalEntity(S entity) {
    S archivalEntity = prepareArchivalEntity(entity);
    saveArchivalEntity(archivalEntity);
  }

  default T enhanceEntity(T t) {
    return t.isUniversalSegment() ? updateUniversal(t) : t;
  }

  default T updateUniversal(T t) {
    t.getInclusionList().add(0, SegmentConstants.UNIVERSAL);
    return t;
  }

  default Set<String> extractSegmentNames(List<SegmentReference> segmentReferences) {
    return segmentReferences.stream()
        .map(SegmentReference::getSegmentName)
        .collect(Collectors.toSet());
  }

  default void isUniversalSegmentChanged(List<T> entities, String segmentName) {
    if (!SegmentConstants.UNIVERSAL.equalsIgnoreCase(segmentName)
        && SegmentConstants.isUniversalSegmentChanged(entities)) {
      entities
          .get(0)
          .setMessage("One or more Universal module(s) have been re-ordered for this Segment");
    }
  }

  default void updateArchivalId(T entity) {

    if (!StringUtils.hasText(entity.getArchivalId()))
      entity.setArchivalId(ObjectId.get().toHexString());
  }

  default void deleteSegments(List<String> segments, String brand) {

    List<T> recordsToUpdate = findAllRecordsBySegmantNameAndBrand(segments, brand);
    if (CollectionUtils.isEmpty(recordsToUpdate)) return;

    recordsToUpdate =
        recordsToUpdate.stream()
            .map(
                (T entity) -> {
                  if (entity.isUniversalSegment()) {
                    entity.setExclusionList(
                        CollectionUtils.isEmpty(entity.getExclusionList())
                            ? new ArrayList<>()
                            : removeSegmentsAndEnchancedList(entity.getExclusionList(), segments));
                  } else {
                    entity.setInclusionList(
                        CollectionUtils.isEmpty(entity.getInclusionList())
                            ? new ArrayList<>()
                            : removeSegmentsAndEnchancedList(entity.getInclusionList(), segments));
                  }
                  return entity;
                })
            .collect(Collectors.toList());

    saveAndUpdateArchivals(recordsToUpdate);
  }

  default List<String> removeSegmentsAndEnchancedList(
      List<String> iteratesegments, List<String> segments) {
    return iteratesegments
        .parallelStream()
        .filter(seg -> !segments.contains(seg))
        .collect(Collectors.toList());
  }

  public abstract List<T> findAllRecordsBySegmantNameAndBrand(List<String> segments, String brand);
}
