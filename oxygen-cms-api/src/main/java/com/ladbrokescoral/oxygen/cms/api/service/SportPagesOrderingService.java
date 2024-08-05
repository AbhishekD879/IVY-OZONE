package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Relation;
import com.ladbrokescoral.oxygen.cms.api.entity.RelationType;
import com.ladbrokescoral.oxygen.cms.api.entity.SortableEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBet;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.SurfaceBetMongoRepository;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@SuppressWarnings("OptionalUsedAsFieldOrParameterType")
@Slf4j
@Service
public class SportPagesOrderingService extends AbstractService<SurfaceBet> {

  private static final Double SORT_ORDER_STEP = 1.0;
  private static final int DIVISION_TWO = 2;
  private static final String HOME_PAGE = "0";

  public static final String SORT_ORDER_FIELD = "references.sortOrder";
  public static final Sort SORT_BY_SORT_ORDER_ASC = Sort.by(SORT_ORDER_FIELD);

  private final SurfaceBetMongoRepository surfaceBetMongoRepository;

  public SportPagesOrderingService(final SurfaceBetMongoRepository surfaceBetMongoRepository) {
    super(surfaceBetMongoRepository);
    this.surfaceBetMongoRepository = surfaceBetMongoRepository;
  }

  public void incrementSortOrderForSportPages(final SurfaceBet surfaceBet) {
    surfaceBet.getReferences().stream()
        .filter(
            ref -> !(ref.getRefId().equals(HOME_PAGE) || ref.getRelatedTo() == RelationType.edp))
        .forEach(
            (Relation ref) -> {
              final String refId = ref.getRefId();
              final Optional<Double> maxSortOrder =
                  findMaxSortOrder(ref.getRelatedTo().name(), refId);

              final Double sortOrder = ref.getSortOrder();
              if (sortOrder != null) {
                ref.setSortOrder(sortOrder);
              } else {
                if (maxSortOrder.isPresent()) {
                  ref.setSortOrder(maxSortOrder.get() + SORT_ORDER_STEP);
                } else {
                  ref.setSortOrder(SORT_ORDER_STEP);
                }
              }
            });
  }

  public Optional<Double> findMaxSortOrder(final String pageType, final String pageId) {

    return surfaceBetMongoRepository.findTheMaxSortOrderOfThePage(pageType, pageId).stream()
        .map(SurfaceBet::getReferences)
        .flatMap(
            ref ->
                ref.stream()
                    .filter(
                        relation ->
                            relation.getRelatedTo().name().equals(pageType)
                                && relation.getRefId().equals(pageId))
                    .map(SortableEntity::getSortOrder))
        .filter(Objects::nonNull)
        .max(Comparator.naturalOrder());
  }

  public void dragAndDropOrder(final OrderDto newOrder) {
    if (StringUtils.isEmpty(newOrder.getId())) {
      throw new IllegalArgumentException("OrderDto.id must not be empty");
    }
    if (CollectionUtils.isEmpty(newOrder.getOrder())) {
      throw new IllegalArgumentException("OrderDto.order must not be empty");
    }

    final String currentElementId = newOrder.getId();
    final int currentElementIndex = newOrder.getOrder().indexOf(currentElementId);

    final Optional<Integer> nexElementIndex =
        getNexElementIndex(currentElementIndex, newOrder.getOrder());
    final Optional<String> nexElementId = nexElementIndex.map(newOrder.getOrder()::get);

    final Optional<Integer> prevElementIndex = getPrevElementIndex(currentElementIndex);
    final Optional<String> prevElementId = prevElementIndex.map(newOrder.getOrder()::get);

    final Optional<SurfaceBet> prevElement = getElementById(prevElementId);
    final SurfaceBet currentElement =
        getElementById(Optional.of(currentElementId)).orElseThrow(NotFoundException::new);
    final Optional<SurfaceBet> nexElement = getElementById(nexElementId);

    final Optional<Double> prevElementSortOrder = getReferencesSortOrder(prevElement, newOrder);
    final Optional<Double> nexElementSortOrder = getReferencesSortOrder(nexElement, newOrder);
    if (isAllElementEmpty(newOrder, currentElement, prevElementSortOrder, nexElementSortOrder)
        || isElementSortOrderNull(nexElement, nexElementSortOrder)
        || isPrevAndNextElementSame(prevElementSortOrder, nexElementSortOrder)) {

      reorderList(newOrder);

    } else {
      Optional<Double> currentElementSortOrder =
          currentElement.getReferences().stream()
              .filter(
                  ref ->
                      newOrder.getPageId().equals(ref.getRefId())
                          && newOrder.getPageType().equals(ref.getRelatedTo().name()))
              .map(SortableEntity::getSortOrder)
              .filter(Objects::nonNull)
              .findFirst();
      buildCurrentElementNewSortOrder(
              prevElementSortOrder, currentElementSortOrder, nexElementSortOrder)
          .ifPresent(
              (Double newSortOrder) -> {
                currentElement.getReferences().stream()
                    .filter(
                        ref ->
                            newOrder.getPageId().equals(ref.getRefId())
                                && newOrder.getPageType().equals(ref.getRelatedTo().name()))
                    .forEach(ref -> ref.setSortOrder(newSortOrder));
                this.save(currentElement);
              });
    }
  }

  private boolean isAllElementEmpty(
      final OrderDto newOrder,
      final SurfaceBet currentElement,
      final Optional<Double> prevElementSortOrder,
      final Optional<Double> nexElementSortOrder) {

    return !prevElementSortOrder.isPresent()
        && !nexElementSortOrder.isPresent()
        && !(currentElement.getReferences().stream()
            .filter(
                ref ->
                    newOrder.getPageId().equals(ref.getRefId())
                        && newOrder.getPageType().equals(ref.getRelatedTo().name()))
            .map(SortableEntity::getSortOrder)
            .anyMatch(Objects::nonNull));
  }

  public boolean isPrevAndNextElementSame(
      final Optional<Double> prevElementSortOrder, final Optional<Double> nextElementSortOrder) {

    return prevElementSortOrder.isPresent()
        && nextElementSortOrder.isPresent()
        && prevElementSortOrder.equals(nextElementSortOrder);
  }

  private boolean isElementSortOrderNull(
      final Optional<SurfaceBet> nexElement, final Optional<Double> nexElementSortOrder) {

    return isNextElementSortOrderNull(nexElement, nexElementSortOrder);
  }

  public Optional<Double> getReferencesSortOrder(
      final Optional<SurfaceBet> element, final OrderDto newOrder) {
    return element
        .map(SurfaceBet::getReferences)
        .flatMap(
            refs ->
                refs.stream()
                    .filter(
                        ref ->
                            newOrder.getPageId().equals(ref.getRefId())
                                && newOrder.getPageType().equals(ref.getRelatedTo().name()))
                    .map(SortableEntity::getSortOrder)
                    .filter(Objects::nonNull)
                    .findFirst());
  }

  public boolean isNextElementSortOrderNull(
      Optional<SurfaceBet> nexElement, Optional<Double> nexElementSortOrder) {
    return nexElement.isPresent() && !nexElementSortOrder.isPresent();
  }

  private void reorderList(OrderDto newOrder) {
    Map<String, Integer> idAndOrder =
        IntStream.range(0, newOrder.getOrder().size())
            .boxed()
            .collect(Collectors.toMap(newOrder.getOrder()::get, idx -> idx));

    List<SurfaceBet> newlySortedOrderList =
        this.findByMatchingIds(newOrder.getOrder()).stream()
            .map(
                (SurfaceBet document) -> {
                  String id = document.getId();
                  Optional.ofNullable(idAndOrder.get(id))
                      .map(Integer::doubleValue)
                      .ifPresent(
                          newSortOrder ->
                              document.getReferences().stream()
                                  .filter(
                                      ref ->
                                          newOrder.getPageId().equals(ref.getRefId())
                                              && newOrder
                                                  .getPageType()
                                                  .equals(ref.getRelatedTo().name()))
                                  .forEach(ref -> ref.setSortOrder(newSortOrder)));
                  return document;
                })
            .collect(Collectors.toList());

    this.saveAndUpdateEntities(newlySortedOrderList);
  }

  private void saveAndUpdateEntities(Iterable<SurfaceBet> entities) {
    repository.saveAll(entities);
  }

  private List<SurfaceBet> findByMatchingIds(List<String> documentIds) {
    return surfaceBetMongoRepository.findByIdMatches(documentIds);
  }

  public Optional<Double> buildCurrentElementNewSortOrder(
      Optional<Double> prevElementSortOrder,
      Optional<Double> currentElementSortOrder,
      Optional<Double> nexElementSortOrder) {

    if (!prevElementSortOrder.isPresent() && !nexElementSortOrder.isPresent()) {
      return currentElementSortOrder;
    }

    if (!prevElementSortOrder.isPresent()) {
      return nexElementSortOrder.map(sortOrder -> sortOrder - SORT_ORDER_STEP);
    }

    if (!nexElementSortOrder.isPresent()) {
      return prevElementSortOrder.map(sortOrder -> sortOrder + SORT_ORDER_STEP);
    }

    Double sortOrder = calculateMidPoint(prevElementSortOrder.get(), nexElementSortOrder.get());

    return Optional.of(sortOrder);
  }

  private Double calculateMidPoint(Double low, Double high) {
    return (low + high) / DIVISION_TWO;
  }

  private Optional<SurfaceBet> getElementById(Optional<String> id) {
    return id.flatMap(this::findOne);
  }

  public Optional<Integer> getNexElementIndex(int currentElementIndex, List<String> list) {
    return Optional.of(currentElementIndex + 1)
        .filter(nextElementIndex -> nextElementIndex < list.size());
  }

  private Optional<Integer> getPrevElementIndex(int currentElementIndex) {
    return Optional.of(currentElementIndex - 1).filter(prevElementIndex -> prevElementIndex >= 0);
  }
}
