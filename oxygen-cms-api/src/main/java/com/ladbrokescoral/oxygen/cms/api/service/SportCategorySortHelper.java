package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.function.ToDoubleFunction;
import java.util.stream.Collectors;
import org.springframework.util.CollectionUtils;

public class SportCategorySortHelper {

  private SportCategorySortHelper() {}

  public static List<SportCategory> sortUniversalRecords(List<SportCategory> universalList) {

    List<SportCategory> segmentReferencesSortOrderRecords =
        universalList
            .parallelStream()
            .filter(
                x ->
                    (!CollectionUtils.isEmpty(x.getSegmentReferences()))
                        && isUniversalSortOrderExsists(x))
            .collect(Collectors.toList());

    List<String> segmentRefIds =
        segmentReferencesSortOrderRecords
            .parallelStream()
            .map(SportCategory::getId)
            .collect(Collectors.toList());

    List<SportCategory> segmentReferencesNOSortOrderRecords =
        universalList
            .parallelStream()
            .filter(segmentRef -> !segmentRefIds.contains(segmentRef.getId()))
            .collect(Collectors.toList());

    segmentReferencesSortOrderRecords =
        sortByOrder(SegmentConstants.UNIVERSAL, segmentReferencesSortOrderRecords);

    segmentReferencesNOSortOrderRecords =
        segmentReferencesNOSortOrderRecords.stream()
            .sorted(SegmentConstants.SPORT_CAT_UNIV_DEFAULT_SORT_ORDER)
            .collect(Collectors.toList());

    segmentReferencesSortOrderRecords.addAll(segmentReferencesNOSortOrderRecords);
    return segmentReferencesSortOrderRecords;
  }

  private static boolean isUniversalSortOrderExsists(SportCategory x) {
    return x.getSegmentReferences().stream()
        .anyMatch(
            ref ->
                SegmentConstants.UNIVERSAL.equalsIgnoreCase(ref.getSegmentName())
                    && ref.getSortOrder() >= 0);
  }

  public static List<SportCategory> sortByOrder(
      String segmentName, List<SportCategory> recordsWithSegmentReference) {

    if (CollectionUtils.isEmpty(recordsWithSegmentReference)) return new ArrayList<>();

    Map<String, SportCategory> mapRecords =
        recordsWithSegmentReference.stream()
            .collect(Collectors.toMap(SportCategory::getId, Function.identity()));

    ToDoubleFunction<SportCategory> sortOrder =
        entity ->
            entity
                .getSegmentReferences()
                .parallelStream()
                .filter(references -> segmentName.equals(references.getSegmentName()))
                .findFirst()
                .get()
                .getSortOrder();

    Map<String, Double> mapSortOrder = new LinkedHashMap<>();
    recordsWithSegmentReference.stream()
        .collect(Collectors.toMap(SportCategory::getId, sortOrder::applyAsDouble))
        .entrySet()
        .stream()
        .sorted(Map.Entry.comparingByValue())
        .forEachOrdered(map -> mapSortOrder.put(map.getKey(), map.getValue()));

    return mapSortOrder.keySet().stream().map(mapRecords::get).collect(Collectors.toList());
  }
}
