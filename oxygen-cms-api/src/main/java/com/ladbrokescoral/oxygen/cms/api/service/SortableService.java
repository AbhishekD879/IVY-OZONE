package com.ladbrokescoral.oxygen.cms.api.service;

import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SortableEntity;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.util.CollectionUtils;
import org.springframework.util.ObjectUtils;

@Slf4j
public abstract class SortableService<T extends SortableEntity> extends AbstractService<T> {

  protected static final Double SORT_ORDER_STEP = 1.0;

  public static final String SORT_ORDER_FIELD = "sortOrder";
  public static final Sort SORT_BY_SORT_ORDER_ASC = Sort.by(SORT_ORDER_FIELD);

  private final CustomMongoRepository<T> mongoRepository;

  public SortableService(CustomMongoRepository<T> mongoRepository) {
    super(mongoRepository);
    this.mongoRepository = mongoRepository;
  }

  @Override
  public List<T> findByBrand(String brand) {
    return mongoRepository.findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  @FortifyXSSValidate("return")
  @Override
  public <S extends T> S save(S entity) {
    incrementSortOrderIfNotSet(entity);
    return mongoRepository.save(entity);
  }

  @Override
  public List<T> save(Iterable<T> entities) {
    return repository.saveAll(entities);
  }

  public void saveAndUpdateArchivals(Iterable<T> entities) {
    repository.saveAll(entities);
  }
  /** Increments #{@code sortOrder} when entity is being created/updated and sortOrder is null */
  protected void incrementSortOrderIfNotSet(T sortableEntity) {
    if (sortableEntity.getSortOrder() == null) {
      incrementSortOrder(sortableEntity);
    }
  }

  /** Increments or decrements #{@code sortOrder} of sortable entity by 1. */
  public void incrementSortOrder(T sortableEntity) {
    Double sortOrder =
        isNewElementCreatedFirstInTheList()
            ? findMinSortOrder(this.mongoRepository) - SORT_ORDER_STEP
            : findMaxSortOrder(this.mongoRepository) + SORT_ORDER_STEP;
    sortableEntity.setSortOrder(sortOrder);
  }

  protected boolean isNewElementCreatedFirstInTheList() {
    return true;
  }

  /**
   * Finds maximum sortOrder value in database for particular collection.
   *
   * @param pagingAndSortingRepository - instance of repository for accessing collection
   */
  private static Double findMaxSortOrder(
      PagingAndSortingRepository<? extends SortableEntity, String> pagingAndSortingRepository) {
    return findSortOrder(pagingAndSortingRepository, Sort.Direction.DESC);
  }

  private static Double findMinSortOrder(
      PagingAndSortingRepository<? extends SortableEntity, String> pagingAndSortingRepository) {
    return findSortOrder(pagingAndSortingRepository, Sort.Direction.ASC);
  }

  private static Double findSortOrder(
      PagingAndSortingRepository<? extends SortableEntity, String> pagingAndSortingRepository,
      Sort.Direction direction) {
    PageRequest requestForElementWithMaxSortOrder =
        PageRequest.of(0, 1, Sort.by(direction, SORT_ORDER_FIELD));
    Page<? extends SortableEntity> sortOrder =
        pagingAndSortingRepository.findAll(requestForElementWithMaxSortOrder);

    // FIXME: `sortOrder == null` is overkill for tests. shame on you.
    return sortOrder == null
            || CollectionUtils.isEmpty(sortOrder.getContent())
            || sortOrder.getContent().get(0).getSortOrder() == null
        ? 0
        : sortOrder.getContent().get(0).getSortOrder();
  }

  public void dragAndDropOrder(OrderDto newOrder) {
    if (StringUtils.isEmpty(newOrder.getId())) {
      throw new IllegalArgumentException("OrderDto.id must not be empty");
    }
    if (CollectionUtils.isEmpty(newOrder.getOrder())) {
      throw new IllegalArgumentException("OrderDto.order must not be empty");
    }

    String currentElementId = newOrder.getId();
    int currentElementIndex = newOrder.getOrder().indexOf(currentElementId);

    Optional<Integer> nexElementIndex =
        getNexElementIndex(currentElementIndex, newOrder.getOrder());
    Optional<String> nexElementId = nexElementIndex.map(newOrder.getOrder()::get);

    Optional<Integer> prevElementIndex = getPrevElementIndex(currentElementIndex);
    Optional<String> prevElementId = prevElementIndex.map(newOrder.getOrder()::get);

    Optional<T> prevElement = getElementById(prevElementId);
    T currentElement =
        getElementById(Optional.of(currentElementId)).orElseThrow(NotFoundException::new);
    Optional<T> nexElement = getElementById(nexElementId);

    Optional<Double> prevElementSortOrder = prevElement.map(T::getSortOrder);
    Optional<Double> nexElementSortOrder = nexElement.map(T::getSortOrder);
    if (isNextElementSortOrderNull(nexElement, nexElementSortOrder)) {
      reorderList(newOrder);

    } else if (prevElementSortOrder.isPresent()
        && nexElementSortOrder.isPresent()
        && prevElementSortOrder.equals(nexElementSortOrder)) {
      // Two elements have the same sortOrder, Impossible to calculate midpoint.Need
      // to recalculate
      // the whole list.
      reorderList(newOrder);
      log.info("Reordered all list for {}", this.getClass().getName());
    } else if (!prevElementSortOrder.isPresent()
        && !nexElementSortOrder.isPresent()
        && ObjectUtils.isEmpty(currentElement.getSortOrder())) {
      reorderList(newOrder);
    } else {
      buildCurrentElementNewSortOrder(
              prevElementSortOrder,
              Optional.ofNullable(currentElement.getSortOrder()),
              nexElementSortOrder)
          .ifPresent(
              newSortOrder -> {
                currentElement.setSortOrder(newSortOrder);
                this.save(currentElement);
              });
    }
  }

  private boolean isNextElementSortOrderNull(
      Optional<T> nexElement, Optional<Double> nexElementSortOrder) {
    return nexElement.isPresent() && !nexElementSortOrder.isPresent();
  }

  public void reorderList(OrderDto newOrder) {
    Map<String, Integer> idAndOrder =
        IntStream.range(0, newOrder.getOrder().size())
            .boxed()
            .collect(Collectors.toMap(newOrder.getOrder()::get, idx -> idx));
    List<T> list =
        this.findByMatchingIds(newOrder.getOrder()).stream()
            .map(
                document -> {
                  String id = document.getId();
                  Optional.ofNullable(idAndOrder.get(id))
                      .map(Integer::doubleValue)
                      .ifPresent(document::setSortOrder);
                  return document;
                })
            .collect(Collectors.toList());
    this.saveAndUpdateArchivals(list);
  }

  public List<T> findByMatchingIds(List<String> documentIds) {
    return mongoRepository.findByIdMatches(documentIds);
  }

  private Optional<Double> buildCurrentElementNewSortOrder(
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

  public Double calculateMidPoint(Double low, Double high) {
    return (low + high) / 2;
  }

  public Optional<T> getElementById(Optional<String> id) {
    return id.flatMap(this::findOne);
  }

  public Optional<Integer> getNexElementIndex(int currentElementIndex, List<String> list) {
    return Optional.of(currentElementIndex + 1)
        .filter(nextElementIndex -> nextElementIndex < list.size());
  }

  public Optional<Integer> getPrevElementIndex(int currentElementIndex) {
    return Optional.of(currentElementIndex - 1).filter(prevElementIndex -> prevElementIndex >= 0);
  }
}
