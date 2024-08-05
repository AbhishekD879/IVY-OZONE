package com.ladbrokescoral.oxygen.cms.api.service.impl;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.HomeModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.HomeModuleArchive;
import com.ladbrokescoral.oxygen.cms.api.entity.DataSelection;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SelectionType;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.exception.BadRequestException;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AbstractSegmentService;
import com.ladbrokescoral.oxygen.cms.api.service.EventHubService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService;
import java.time.Instant;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import javax.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class HomeModuleServiceImpl extends AbstractSegmentService<HomeModule> {

  public static final Sort SORT_BY_DISPLAY_ORDER_ASC = Sort.by("sortOrder");

  private final HomeModuleRepository homeModuleRepository;

  private EventHubService hubService;

  private ModelMapper modelMapper;

  public HomeModuleServiceImpl(
      HomeModuleRepository homeModuleRepository,
      HomeModuleArchivalRepository homeModuleArchivalRepository,
      ModelMapper modelMapper,
      SegmentService segmentService,
      EventHubService hubService) {
    super(homeModuleRepository, homeModuleArchivalRepository, segmentService);
    this.modelMapper = modelMapper;
    this.homeModuleRepository = homeModuleRepository;
    this.hubService = hubService;
  }

  @Override
  public List<HomeModule> findByBrand(String brand) {
    return homeModuleRepository.findByBrand(brand, SORT_BY_DISPLAY_ORDER_ASC);
  }

  public List<HomeModule> findByActiveState(boolean active) {
    return active
        ? homeModuleRepository.findAllActive(Instant.now())
        : homeModuleRepository.findAllInactive(Instant.now());
  }

  public List<HomeModule> findByActiveStateAndPublishToChannel(boolean isActive, String brand) {
    return isActive
        ? homeModuleRepository.findAllActiveAndPublishToChannel(
            Instant.now(), brand, SORT_BY_DISPLAY_ORDER_ASC)
        : homeModuleRepository.findAllInactiveAndPublishToChannel(
            Instant.now(), brand, SORT_BY_DISPLAY_ORDER_ASC);
  }

  public List<HomeModule> findAll(String brand, PageType pageType, String pageId) {
    return homeModuleRepository.findAll(brand, pageType, pageId, SORT_BY_DISPLAY_ORDER_ASC);
  }

  @Override
  public HomeModule prepareModelBeforeSave(HomeModule model) {
    if (!model.isMultiBranded() && model.getBrandsCount() != 1) {
      throw new IllegalArgumentException("Please provide only one brand in published devices");
    }
    validateDataSelectionId(model);
    if (isLinkedToEventHub(model)) {
      validateEventHub(model);
    }
    if (model.isGroupedBySport() && model.isHero()) {
      throw new BadRequestException("Only ungrouped module can be hero");
    }
    validateAutoRefresh(model);
    return super.prepareModelBeforeSave(model);
  }

  private void validateDataSelectionId(HomeModule model) {
    DataSelection dataSelection = model.getDataSelection();
    if (!SelectionType.RACE_TYPE_ID.getValue().equals(dataSelection.getSelectionType())
        && dataSelection.getSelectionId().contains(",")) {
      throw new IllegalArgumentException("DataSelection should be a number");
    }
  }

  private void validateAutoRefresh(HomeModule model) {
    if (model.getEventsSelectionSettings().isAutoRefresh()
        && !SelectionType.isAutoRefreshSupported(model.getDataSelection().getSelectionType())) {
      throw new IllegalArgumentException("Cannot auto-refresh events with the SelectionType");
    }
  }

  private boolean isLinkedToEventHub(HomeModule model) {
    return PageType.eventhub.equals(model.getPageType());
  }

  private void validateEventHub(HomeModule model) {
    Integer indexNumber = Integer.valueOf(model.getPageId());
    String brand = model.getBrand();
    if (!hubService.existByBrandAndIndexNumber(brand, indexNumber)) {
      throw new IllegalArgumentException(
          "Invalid eventHubId : " + model.getPageId() + " for brand : " + brand);
    }
  }

  @Override
  public HomeModuleArchive prepareArchivalEntity(HomeModule entity) {
    return modelMapper.map(entity, HomeModuleArchive.class);
  }

  @Override
  public void delete(String id) {
    Optional<HomeModule> point = findOne(id);
    if (point.isPresent()) {
      HomeModuleArchive archive = prepareArchivalEntity(point.get());
      archive.setDeleted(true);
      super.saveArchivalEntity(archive);
      super.delete(id);
    }
  }

  public List<HomeModule> findByActiveStateAndPublishToChannelBySegmantName(
      boolean active, String brand, String segmentName) {

    List<HomeModule> records =
        SegmentConstants.UNIVERSAL.equalsIgnoreCase(segmentName)
            ? getUniversal(brand, active)
            : getSegmentAndUniversal(brand, segmentName, active);

    return records.stream().map(this::enhanceEntity).collect(Collectors.toList());
  }

  private List<HomeModule> getSegmentAndUniversal(
      String brand, String segmentName, boolean active) {

    return active
        ? getActiveSegmentModules(brand, segmentName, active)
        : homeModuleRepository.findAllUniversalAndSegmentInActiveAndPublishToChannel(
            Instant.now(), brand, active, Arrays.asList(segmentName), SORT_BY_DISPLAY_ORDER_ASC);
  }

  private List<HomeModule> getActiveSegmentModules(
      String brand, String segmentName, boolean active) {
    List<HomeModule> recordsWithSegmentReference =
        homeModuleRepository.findAllPublishToChannelAndSegmentNameAndIsActive(
            Instant.now(), brand, Arrays.asList(segmentName), active, SORT_BY_DISPLAY_ORDER_ASC);
    recordsWithSegmentReference = super.sortByOrder(segmentName, recordsWithSegmentReference);
    // check universal segment changed or not...
    isUniversalSegmentChanged(recordsWithSegmentReference, segmentName);
    List<String> inclusiveListIds =
        recordsWithSegmentReference.stream().map(HomeModule::getId).collect(Collectors.toList());
    List<HomeModule> universalList =
        homeModuleRepository
            .findByPublishToChannelAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
                Instant.now(),
                brand,
                Arrays.asList(segmentName),
                inclusiveListIds,
                active,
                SORT_BY_DISPLAY_ORDER_ASC);

    recordsWithSegmentReference.addAll(universalList);
    return recordsWithSegmentReference;
  }

  private List<HomeModule> getUniversal(String brand, boolean active) {
    return active
        ? homeModuleRepository.findAllUniversalActiveAndPublishToChannel(
            Instant.now(), brand, active, SORT_BY_DISPLAY_ORDER_ASC)
        : homeModuleRepository.findAllUniversalInActiveAndPublishToChannel(
            Instant.now(), brand, active, SORT_BY_DISPLAY_ORDER_ASC);
  }

  public List<HomeModule> findAll(
      String brand, @Valid PageType pageType, String pageId, String segmentName) {

    List<HomeModule> records =
        SegmentConstants.UNIVERSAL.equalsIgnoreCase(segmentName)
            ? getUniversal(brand, pageType, pageId)
            : getSegmentAndUniversal(brand, segmentName, pageType, pageId);

    return records.stream().map(this::enhanceEntity).collect(Collectors.toList());
  }

  private List<HomeModule> getSegmentAndUniversal(
      String brand, String segmentName, @Valid PageType pageType, String pageId) {

    List<HomeModule> recordsWithSegmentReference =
        homeModuleRepository.findAllSegmentByBrandAndPageIdAndPageType(
            brand, pageType, pageId, segmentName, SORT_BY_DISPLAY_ORDER_ASC);
    recordsWithSegmentReference = super.sortByOrder(segmentName, recordsWithSegmentReference);

    List<String> inclusiveListIds =
        recordsWithSegmentReference.stream().map(HomeModule::getId).collect(Collectors.toList());
    List<HomeModule> universalList =
        homeModuleRepository
            .findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveListAndPageIdAndPageType(
                brand,
                Arrays.asList(segmentName),
                inclusiveListIds,
                pageType,
                pageId,
                SORT_BY_DISPLAY_ORDER_ASC);

    recordsWithSegmentReference.addAll(universalList);
    return recordsWithSegmentReference;
  }

  private List<HomeModule> getUniversal(String brand, @Valid PageType pageType, String pageId) {
    return homeModuleRepository.findAllUniversalByBrandAndPageIdAndPageType(
        brand, pageType, pageId, SORT_BY_DISPLAY_ORDER_ASC);
  }

  public List<HomeModule> findByActiveStateAndPublishToChannelAndApplyUniversalSegments(
      boolean active, String brand) {
    return active
        ? homeModuleRepository.findAllActiveAndPublishToChannelAndApplyUniversalSegments(
            Instant.now(), brand, SORT_BY_DISPLAY_ORDER_ASC)
        : homeModuleRepository.findAllInactiveAndPublishToChannelAndApplyUniversalSegments(
            Instant.now(), brand, SORT_BY_DISPLAY_ORDER_ASC);
  }

  @Override
  public HomeModule saveEntity(HomeModule entity) {
    if (!"0".equals(entity.getPageId())) {
      entity.setSortOrder(entity.getDisplayOrder());
    } else {
      entity.setDisplayOrder(entity.getSortOrder());
    }
    return super.saveEntity(entity);
  }

  @Override
  public List<HomeModule> findAllRecordsBySegmantNameAndBrand(List<String> segments, String brand) {

    return homeModuleRepository.findAllBySegmentNameIninclusiveAndExclusiveAndPulishToChannels(
        brand, segments);
  }
}
