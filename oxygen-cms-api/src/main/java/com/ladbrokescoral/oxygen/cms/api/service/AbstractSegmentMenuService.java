package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.CustomArchivalMongoRepository;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.AbstractMenuSegmentEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomSegmentRepository;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.util.StringUtils;

@Slf4j
public abstract class AbstractSegmentMenuService<T extends AbstractMenuSegmentEntity>
    extends AbstractMenuService<T> implements SegmentedService<T> {

  private final CustomSegmentRepository<T> segmentedRepository;

  private CustomArchivalMongoRepository<? extends T> archivalRepository;
  protected SegmentService segmentService;

  protected AbstractSegmentMenuService(
      CustomSegmentRepository<T> mongoRepository,
      CustomArchivalMongoRepository<? extends T> navigationPointArchivalRepository,
      SegmentService segmentService) {
    super(mongoRepository);
    this.archivalRepository = navigationPointArchivalRepository;
    this.segmentedRepository = mongoRepository;
    this.segmentService = segmentService;
  }

  @Override
  public <S extends T> S save(S entity) {

    return SegmentedService.super.save(entity);
  }

  public <S extends T> S saveEntity(S entity) {

    return super.save(entity);
  }

  @Override
  public void createSegments(List<String> segments, String brand) {

    segmentService.createSegments(segments, brand);
  }

  @Override
  public void dragAndDropOrder(OrderDto newOrder) {
    if (!StringUtils.hasText(newOrder.getSegmentName())
        || SegmentConstants.UNIVERSAL.equals(newOrder.getSegmentName())) {
      super.dragAndDropOrder(newOrder);
    } else {
      SegmentedService.super.dragAndDropOrder(newOrder);
    }
  }

  public <S extends T> void saveArchivalEntity(S archivalEntity) {
    archivalRepository.save(enhanceArchivalEntity(archivalEntity));
  }

  public List<T> getUniversal(String brand, Optional<String> deviceType) {

    return !deviceType.isPresent()
        ? segmentedRepository.findUniversalRecordsByBrand(
            brand, SortableService.SORT_BY_SORT_ORDER_ASC)
        : segmentedRepository.findUniversalRecordsByBrandAndDeviceType(
            brand, deviceType.get(), SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  public List<T> getAllRecordsBySegmentName(
      String brand, String segmentName, Optional<String> deviceType) {
    return !deviceType.isPresent()
        ? segmentedRepository.findAllByBrandAndSegmentName(brand, Arrays.asList(segmentName))
        : segmentedRepository.findAllByBrandAndSegmentNameAndDeviceType(
            brand, Arrays.asList(segmentName), deviceType.get());
  }

  /**
   * find all the records by (Universal :true and segment name not in Exclusion List) or (in
   * inclusion list and not in segment references) order by sort order
   */
  @Override
  public List<T> findAllUniversalAndNotInsegmentReferences(
      String brand, String segmentName, List<String> inclusiveIds, Optional<String> deviceType) {

    return !deviceType.isPresent()
        ? findAllUniversalAndNotInsegmentReferences(brand, segmentName, inclusiveIds)
        : findAllUniversalAndNotInsegmentReferences(
            brand, segmentName, inclusiveIds, deviceType.get());
  }

  private List<T> findAllUniversalAndNotInsegmentReferences(
      String brand, String segmentName, List<String> inclusiveIds) {
    return segmentedRepository
        .findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
            brand,
            Arrays.asList(segmentName),
            inclusiveIds,
            SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  private List<T> findAllUniversalAndNotInsegmentReferences(
      String brand, String segmentName, List<String> inclusiveIds, String deviceType) {
    return segmentedRepository
        .findByBrandAndDeviceTypeAndApplyUniversalSegmentsAndNotInExclusionListAndInInclusiveList(
            brand,
            Arrays.asList(segmentName),
            inclusiveIds,
            deviceType,
            SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  @Override
  public boolean isNewElementCreatedFirstInTheList() {
    return false;
  }

  @Override
  public void saveAndUpdateArchivals(Iterable<T> list) {
    list.forEach(SegmentedService.super::updateArchivalId);
    List<T> entities = super.save(list);
    entities.stream()
        .parallel()
        .forEach(archival -> saveArchivalEntity(prepareArchivalEntity(archival)));
  }

  @Override
  public List<T> findAllRecordsBySegmantNameAndBrand(List<String> segments, String brand) {

    return segmentedRepository.findAllBySegmentNameIninclusiveAndExclusive(brand, segments);
  }
}
