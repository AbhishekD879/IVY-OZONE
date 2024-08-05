package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.OptionalInt;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;

public interface SegmentedSortService<T extends SegmentEntity> {

  static final Double DEFAULT_SORT_ORDER_STEP = -1.0;
  static final Double INITIAL_SORT_ORDER_STEP = 0.0;
  static final Integer SPACE_SORT_ORDER_STEP = 100;

  public Optional<T> getElementById(Optional<String> id);

  public List<T> findByMatchingIds(List<String> documentIds);

  public <S extends T> S save(S entity);

  public void saveAndUpdateArchivals(Iterable<T> list);

  public Optional<Integer> getNexElementIndex(int currentElementIndex, List<String> list);

  public Optional<Integer> getPrevElementIndex(int currentElementIndex);

  public Double calculateMidPoint(Double low, Double high);

  default void dragAndDropOrder(OrderDto newOrder) {
    if (!StringUtils.hasText(newOrder.getId())) {
      throw new IllegalArgumentException("OrderDto.id must not be empty");
    }
    if (CollectionUtils.isEmpty(newOrder.getOrder())) {
      throw new IllegalArgumentException("OrderDto.order must not be empty");
    }

    String segmentName = newOrder.getSegmentName();
    String currentElementId = newOrder.getId();
    int currentElementIndex = newOrder.getOrder().indexOf(currentElementId);

    Optional<Integer> nexElementIndex =
        getNexElementIndex(currentElementIndex, newOrder.getOrder());
    Optional<String> nexElementId = nexElementIndex.map(newOrder.getOrder()::get);

    Optional<Integer> prevElementIndex = getPrevElementIndex(currentElementIndex);
    Optional<String> prevElementId = prevElementIndex.map(newOrder.getOrder()::get);

    Optional<T> prevElement = getElementById(prevElementId);
    Optional<Double> minSortOrder = getListOfRecordTobeProcessed(currentElementIndex, newOrder);

    List<String> tobeInserted = new ArrayList<>();

    // Building new order list computing what are all the elements to be sorted

    newOrder
        .getIndexId()
        .ifPresent(
            x ->
                tobeInserted.addAll(
                    newOrder
                        .getOrder()
                        .subList(newOrder.getIndexId().get(), currentElementIndex + 1)));

    T currentElement =
        getElementById(Optional.of(currentElementId)).orElseThrow(NotFoundException::new);

    Optional<T> nexElement = getElementById(nexElementId);

    Optional<Double> prevElementSortOrder = getSortNumber(prevElement, newOrder);
    Optional<Double> nexElementSortOrder = getSortNumber(nexElement, newOrder);
    Optional<Double> curElementSortOrder = getSortNumber(Optional.of(currentElement), newOrder);

    if (tobeInserted.size() > 1) {
      newOrder.setOrder(tobeInserted);
      buildSegmentElementSortOrder(newOrder, minSortOrder, nexElementSortOrder);

    } else if (isNextAndPreviousSortOrderSame(prevElementSortOrder, nexElementSortOrder)
        || (nexElementSortOrder.isPresent()
            && INITIAL_SORT_ORDER_STEP.equals(nexElementSortOrder.get()))) {
      reorderSegmentList(newOrder);
    } else {

      buildCurrentElementNewSegmentSortOrder(
              prevElementSortOrder, curElementSortOrder, nexElementSortOrder)
          .ifPresent(
              (Double newSortOrder) -> {
                String pageRef = getPageRef(currentElement, newOrder);
                updateNewSortOrder(currentElement, newSortOrder, segmentName, pageRef);
                this.save(currentElement);
              });
    }
  }

  default boolean isNextAndPreviousSortOrderSame(
      Optional<Double> prevElementSortOrder, Optional<Double> nexElementSortOrder) {
    return prevElementSortOrder.isPresent()
        && nexElementSortOrder.isPresent()
        && prevElementSortOrder.equals(nexElementSortOrder);
  }

  default OptionalInt getIndexBySegmentName(
      List<SegmentReference> list, String segmentName, String pageRef) {

    return StringUtils.hasText(pageRef)
        ? IntStream.range(0, list.size())
            .filter(
                i ->
                    list.get(i).getSegmentName().equals(segmentName)
                        && pageRef.equals(list.get(i).getPageRefId()))
            .findFirst()
        : IntStream.range(0, list.size())
            .filter(i -> list.get(i).getSegmentName().equals(segmentName))
            .findFirst();
  }

  default void updateNewSortOrder(
      T currentElement, Double newSortOrder, String segmentName, String pageRef) {

    List<SegmentReference> segmentReferences = currentElement.getSegmentReferences();
    OptionalInt segmentIndex = getIndexBySegmentName(segmentReferences, segmentName, pageRef);

    if (segmentIndex.isPresent()) {
      segmentReferences.get(segmentIndex.getAsInt()).updateSortOrder(newSortOrder);
    } else {
      segmentReferences.add(buildSegmentReference(segmentName, newSortOrder, pageRef));
    }
  }

  public default Optional<Double> getSortNumber(Optional<T> element, OrderDto orderDto) {

    return element.isPresent() && !CollectionUtils.isEmpty(element.get().getSegmentReferences())
        ? element.get().getSegmentReferences().stream()
            .filter(isSegmentExists(orderDto.getSegmentName()))
            .filter(x -> x.getSortOrder() >= 0)
            .map(SegmentReference::getSortOrder)
            .findFirst()
        : Optional.empty();
  }

  public default Predicate<SegmentReference> isSegmentExists(String segmentName) {

    return segmentReference -> segmentName.equals(segmentReference.getSegmentName());
  }

  public default void buildSegmentElementSortOrder(
      OrderDto newOrder, Optional<Double> minSortOrder, Optional<Double> nexElementSortOrder) {
    if (isNextAndPreviousSortOrderSame(nexElementSortOrder, minSortOrder)
        || (!nexElementSortOrder.isPresent() && !minSortOrder.isPresent())) {

      reorderSegmentList(newOrder); // order from 0 to max list value

    } else {
      reorderList(newOrder, minSortOrder, nexElementSortOrder); // reOrder By prevsort value
    }
  }

  public default void reorderSegmentList(OrderDto newOrder) {
    Map<String, Double> idAndOrder =
        IntStream.range(0, newOrder.getOrder().size())
            .boxed()
            .collect(Collectors.toMap(newOrder.getOrder()::get, this::getNextDouble));
    updateSortOrderAndSave(newOrder, idAndOrder);
  }

  public default void updateSortOrderAndSave(
      OrderDto idsToBeSorted, Map<String, Double> idAndOrder) {
    List<T> list =
        this.findByMatchingIds(idsToBeSorted.getOrder()).stream()
            .map(document -> enhanceDocument(idsToBeSorted, idAndOrder, document))
            .collect(Collectors.toList());
    saveAndUpdateArchivals(list);
  }

  public default Optional<Double> buildCurrentElementNewSegmentSortOrder(
      Optional<Double> prevElementSortOrder,
      Optional<Double> currentElementSortOrder,
      Optional<Double> nexElementSortOrder) {
    if (!prevElementSortOrder.isPresent() && !nexElementSortOrder.isPresent()) {
      return currentElementSortOrder.isPresent()
          ? currentElementSortOrder
          : Optional.of(SPACE_SORT_ORDER_STEP.doubleValue());
    }

    if (!prevElementSortOrder.isPresent()) {
      return nexElementSortOrder.map(
          sortOrder -> calculateMidPoint(INITIAL_SORT_ORDER_STEP, sortOrder));
    }

    if (!nexElementSortOrder.isPresent()) {
      return prevElementSortOrder.map(sortOrder -> sortOrder + SPACE_SORT_ORDER_STEP.doubleValue());
    }
    Double sortOrder = calculateMidPoint(prevElementSortOrder.get(), nexElementSortOrder.get());
    return Optional.of(sortOrder);
  }

  public default T enhanceDocument(OrderDto newOrder, Map<String, Double> idAndOrder, T document) {
    String id = document.getId();
    document.getSegmentReferences().stream()
        .forEach(
            (SegmentReference references) -> {
              if (newOrder.getSegmentName().equals(references.getSegmentName())) {
                Optional.ofNullable(idAndOrder.get(id)).ifPresent(references::updateSortOrder);
              }
            });
    if (document.getSegmentReferences().stream()
        .noneMatch(isSegmentExists(newOrder.getSegmentName()))) {
      String pageRef = getPageRef(document, newOrder);
      document
          .getSegmentReferences()
          .add(
              buildSegmentReference(
                  newOrder.getSegmentName(),
                  Optional.ofNullable(idAndOrder.get(id)).orElse(null),
                  pageRef));
    }
    return document;
  }

  public default String getPageRef(T element, OrderDto orderDto) {
    return null;
  }

  public default SegmentReference buildSegmentReference(String segmentName, Double sortOrder) {
    User user = (User) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
    return SegmentReference.builder()
        .sortOrder(sortOrder)
        .segmentName(segmentName)
        .createdAt(Instant.now())
        .updatedAt(Instant.now())
        .createdBy(user.getId())
        .updatedBy(user.getId())
        .build();
  }

  public default SegmentReference buildSegmentReference(
      String segmentName, Double sortOrder, String pageRefId) {
    User user = (User) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
    return SegmentReference.builder()
        .sortOrder(sortOrder)
        .segmentName(segmentName)
        .createdAt(Instant.now())
        .updatedAt(Instant.now())
        .createdBy(user.getId())
        .updatedBy(user.getId())
        .pageRefId(pageRefId)
        .build();
  }

  public default void reorderList(
      OrderDto idsToBeSorted, Optional<Double> minOrder, Optional<Double> maxOrder) {

    Map<String, Double> idAndOrder = new HashMap<>();
    Double min = ifMinOrderPresentOrElse(minOrder);
    for (String string : idsToBeSorted.getOrder()) {
      if (maxOrder.isPresent()) {
        min = calculateMidPoint(min, maxOrder.get());
      } else {
        min = min + SPACE_SORT_ORDER_STEP.doubleValue();
      }
      idAndOrder.put(string, min);
    }
    updateSortOrderAndSave(idsToBeSorted, idAndOrder);
  }

  public default Double ifMinOrderPresentOrElse(Optional<Double> minOrder) {
    return minOrder.isPresent() ? minOrder.get() : INITIAL_SORT_ORDER_STEP;
  }

  default Double getNextDouble(Integer t) {
    // DisplayOrder starts from 100 .initial space is 100
    t = (t + 1) * SPACE_SORT_ORDER_STEP;
    return t.doubleValue();
  }

  /**
   * Recursivly check for the minsort order for already sorted record if exsists else return empty
   * and find the index of new order from where to sort the ids
   */
  default Optional<Double> getListOfRecordTobeProcessed(
      int currentElementIndex, OrderDto newOrder) {

    Optional<Integer> prevElementIndex = getPrevElementIndex(currentElementIndex);
    Optional<String> prevElementId = prevElementIndex.map(newOrder.getOrder()::get);

    Optional<T> prevElement = getElementById(prevElementId);

    if (prevElement.isPresent()) {

      Optional<SegmentReference> segmentReference =
          getSegmentReferenceBySegmentName(prevElement.get(), newOrder);

      if (!segmentReference.isPresent()
          || DEFAULT_SORT_ORDER_STEP.equals(segmentReference.get().getSortOrder())) {
        int prevcurrentElementIndex = newOrder.getOrder().indexOf(prevElementId.orElse(null));
        newOrder.setIndexId(prevElementIndex);
        return getListOfRecordTobeProcessed(prevcurrentElementIndex, newOrder);

      } else {
        return segmentReference.map(SegmentReference::getSortOrder); // min sortoRDER
      }
    }
    return Optional.empty();
  }

  default Optional<SegmentReference> getSegmentReferenceBySegmentName(
      T prevElement, OrderDto orderDto) {
    return prevElement.getSegmentReferences().stream()
        .filter(isSegmentExists(orderDto.getSegmentName()))
        .filter(x -> x.getSortOrder() >= 0)
        .findFirst();
  }
}
