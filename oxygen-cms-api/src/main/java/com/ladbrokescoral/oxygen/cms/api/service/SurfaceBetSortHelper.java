package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.api.entity.AbstractSportEntity.SPORT_HOME_PAGE;

import com.ladbrokescoral.oxygen.cms.api.dto.SurfaceBetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Relation;
import com.ladbrokescoral.oxygen.cms.api.entity.RelationType;
import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBet;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;

public class SurfaceBetSortHelper {

  private static final int ONE_THOUSAND = 1000;
  private static final int ONE = 1;

  private SurfaceBetSortHelper() {}

  // segmentReferencesRecords :filter All Surface bets by universal segment exsists and sorder
  // greater than 0 this are sorted records
  // nonSegmentReferencesRecords:filter All Surface bets not in segmentReferencesRecords
  // segmentReferencesSortOrderRecords to be sorted by segmentName
  // segmentReferencesNOSortOrderRecords to be sorted by the Created date

  public static List<SurfaceBet> sortSurfaceBetUniversalRecords(
      List<SurfaceBet> universalList, RelationType valueOf, String pageId) {

    List<SurfaceBet> segmentReferencesSortOrderRecords =
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
            .map(SurfaceBet::getId)
            .collect(Collectors.toList());

    List<SurfaceBet> segmentReferencesNOSortOrderRecords =
        universalList
            .parallelStream()
            .filter(segmentRef -> !segmentRefIds.contains(segmentRef.getId()))
            .collect(Collectors.toList());

    segmentReferencesSortOrderRecords =
        sortByOrder(
            SegmentConstants.UNIVERSAL,
            segmentReferencesSortOrderRecords,
            Relation.builder().relatedTo(valueOf).refId(pageId).build());

    segmentReferencesNOSortOrderRecords =
        segmentReferencesNOSortOrderRecords.stream()
            .sorted(SegmentConstants.SURFACE_BET_UNIV_DEFAULT_SORT_ORDER)
            .collect(Collectors.toList());
    segmentReferencesSortOrderRecords.addAll(segmentReferencesNOSortOrderRecords);
    return segmentReferencesSortOrderRecords;
  }

  private static boolean isUniversalSortOrderExsists(SurfaceBet x) {
    return x.getSegmentReferences().stream()
        .anyMatch(
            ref ->
                SegmentConstants.UNIVERSAL.equalsIgnoreCase(ref.getSegmentName())
                    && ref.getSortOrder() >= 0);
  }

  public static List<SurfaceBet> sortByOrder(
      String segmentName, List<SurfaceBet> recordsWithSegmentReference, Relation relation) {
    if (CollectionUtils.isEmpty(recordsWithSegmentReference)) return new ArrayList<>();

    Map<String, SurfaceBet> mapRecords =
        recordsWithSegmentReference.stream()
            .collect(Collectors.toMap(SurfaceBet::getId, Function.identity()));

    Map<String, String> mapReferences =
        recordsWithSegmentReference.stream()
            .collect(
                HashMap::new,
                (m, v) -> m.put(v.getId(), getRelationId(v, relation)),
                HashMap::putAll);

    Map<String, Double> mapSortOrder = new LinkedHashMap<>();
    recordsWithSegmentReference.stream()
        .collect(
            Collectors.toMap(
                SurfaceBet::getId,
                entity -> getSortOrder(entity, segmentName, mapReferences.get(entity.getId()))))
        .entrySet()
        .stream()
        .sorted(Map.Entry.comparingByValue())
        .forEachOrdered(map -> mapSortOrder.put(map.getKey(), map.getValue()));

    return mapSortOrder.keySet().stream().map(mapRecords::get).collect(Collectors.toList());
  }

  private static Double getSortOrder(SurfaceBet entity, String segmentName, String pageRef) {

    return StringUtils.hasText(pageRef)
        ? entity
            .getSegmentReferences()
            .parallelStream()
            .filter(
                references ->
                    segmentName.equals(references.getSegmentName())
                        && pageRef.equals(references.getPageRefId()))
            .findFirst()
            .map(SegmentReference::getSortOrder)
            .orElse(0.0)
        : -1.0;
  }

  private static String getRelationId(SurfaceBet surfaceBet, Relation relation) {

    return CollectionUtils.isEmpty(surfaceBet.getReferences())
        ? null
        : surfaceBet.getReferences().stream()
            .filter(
                ref ->
                    relation.getRefId().equals(ref.getRefId())
                        && relation.getRelatedTo().equals(ref.getRelatedTo()))
            .findFirst()
            .map(Relation::getId)
            .orElse(null);
  }

  public static List<SurfaceBetDto> getHomeAndReamingSportPagesSortedOrder(
      final List<SurfaceBetDto> surfaceBetDtoList) {

    final List<SurfaceBetDto> sortedOrderList = getPageWiseSortedSurfaceBets(surfaceBetDtoList);

    final List<SurfaceBetDto> nullSortOrderSurfaceBets =
        getNullSortOrderSurfaceBets(surfaceBetDtoList);

    return Stream.of(sortedOrderList, nullSortOrderSurfaceBets)
        .flatMap(Collection::stream)
        .collect(Collectors.toList());
  }

  private static List<SurfaceBetDto> getPageWiseSortedSurfaceBets(
      final List<SurfaceBetDto> surfaceBetDtoList) {

    final List<SurfaceBetDto> homePageSurfaceBets =
        surfaceBetDtoList.stream()
            .filter(
                surfaceBetDto -> surfaceBetDto.getReference().getRefId().equals(SPORT_HOME_PAGE))
            .collect(Collectors.toList());

    final Set<String> sportPages =
        surfaceBetDtoList.stream()
            .map(surfaceBetDto -> surfaceBetDto.getReference().getRefId())
            .filter(pageId -> !(pageId.equals(SPORT_HOME_PAGE)))
            .collect(Collectors.toSet());

    final List<SurfaceBetDto> sportPagesSurfaceBets = new ArrayList<>();
    sportPages.forEach(
        (String sportPage) -> {
          final AtomicInteger count = new AtomicInteger(ONE);
          final List<SurfaceBetDto> pageWiseSurfaceBets =
              surfaceBetDtoList.stream()
                  .filter(
                      surfaceBetDto ->
                          surfaceBetDto.getReference().getRefId().equals(sportPage)
                              && surfaceBetDto.getReference().getSortOrder() != null)
                  .sorted(
                      Comparator.comparingDouble(
                          surfaceBet -> surfaceBet.getReference().getSortOrder()))
                  .map(
                      (SurfaceBetDto surfaceBetDto) -> {
                        surfaceBetDto.setDisplayOrder(count.getAndIncrement());
                        return surfaceBetDto;
                      })
                  .collect(Collectors.toList());

          count.set(ONE);
          sportPagesSurfaceBets.addAll(pageWiseSurfaceBets);
        });

    return Stream.of(homePageSurfaceBets, sportPagesSurfaceBets)
        .flatMap(Collection::stream)
        .collect(Collectors.toList());
  }

  private static List<SurfaceBetDto> getNullSortOrderSurfaceBets(
      final List<SurfaceBetDto> surfaceBetDtoList) {

    final AtomicInteger count = new AtomicInteger(ONE_THOUSAND);
    final List<SurfaceBetDto> nullSurfaceBets =
        surfaceBetDtoList.stream()
            .filter(
                surfaceBetDto -> !surfaceBetDto.getReference().getRefId().equals(SPORT_HOME_PAGE))
            .filter(surfaceBetDto -> surfaceBetDto.getReference().getSortOrder() == null)
            .map(
                (SurfaceBetDto surfaceBetDto) -> {
                  surfaceBetDto.setDisplayOrder(count.getAndIncrement());
                  return surfaceBetDto;
                })
            .collect(Collectors.toList());
    count.set(ONE_THOUSAND);

    return nullSurfaceBets;
  }
}
