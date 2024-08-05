package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.FooterMenuArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.FooterMenuArchive;
import com.ladbrokescoral.oxygen.cms.api.dto.FooterMenuSegmentedDto;
import com.ladbrokescoral.oxygen.cms.api.entity.DeviceType;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.mapping.FooterMenuMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.FooterMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Component
@Validated
public class FooterMenuService extends AbstractSegmentMenuService<FooterMenu> {

  private final FooterMenuRepository footerMenuRepository;
  private final ImageEntityService<FooterMenu> imageEntityService;
  private final SvgEntityService<FooterMenu> svgEntityService;
  private ModelMapper modelMapper;

  private static final int DEFAULT_QUERY_LIMIT = 5;
  private static final int RCOMB_CONNECT_QUERY_LIMIT = 6;
  private final ImagePath footerMenuImagePath;
  private final SegmentedModuleSerive segmentedModuleSerive;

  @Autowired
  public FooterMenuService(
      FooterMenuRepository repository,
      ImageEntityService<FooterMenu> imageEntityService,
      SvgEntityService<FooterMenu> svgEntityService,
      ImagePath footerMenuImagePath,
      ModelMapper modelMapper,
      FooterMenuArchivalRepository footerMenuArchivalRepository,
      SegmentService segmentService,
      SegmentedModuleSerive segmentedModuleSerive) {
    super(repository, footerMenuArchivalRepository, segmentService);

    this.footerMenuRepository = repository;
    this.imageEntityService = imageEntityService;
    this.svgEntityService = svgEntityService;
    this.footerMenuImagePath = footerMenuImagePath;
    this.modelMapper = modelMapper;
    this.segmentedModuleSerive = segmentedModuleSerive;
  }

  public List<FooterMenuSegmentedDto> findAllActiveByBrand(String brand) {
    PageRequest pageRequest =
        PageRequest.of(0, Integer.MAX_VALUE, SortableService.SORT_BY_SORT_ORDER_ASC);
    List<FooterMenu> footerMenus =
        footerMenuRepository.findAllActiveRecordsByBrand(brand, pageRequest);

    List<String> segments = segmentService.getSegmentsForSegmentedViews(brand);
    return footerMenus.stream()
        .map(e -> FooterMenuMapper.INSTANCE.toSegmentedDto(e, segments))
        .collect(Collectors.toList());
  }

  public List<FooterMenu> findAllByBrandAndDisabled(String brand) {
    PageRequest pageRequest =
        PageRequest.of(0, Integer.MAX_VALUE, SortableService.SORT_BY_SORT_ORDER_ASC);
    return footerMenuRepository.findUniversalRecordsByBrand(brand, false, pageRequest);
  }

  public List<FooterMenu> findAllByBrandAndDeviceType(String brand, String deviceType) {
    DeviceType queryDeviceType = DeviceType.fromString(deviceType).orElse(DeviceType.MOBILE);
    PageRequest pageRequest =
        PageRequest.of(
            0, getQueryLimit(brand, queryDeviceType), SortableService.SORT_BY_SORT_ORDER_ASC);

    return footerMenuRepository.findUniversalRecordsByBrand(
        brand, queryDeviceType.getValue(), true, pageRequest);
  }

  public List<FooterMenu> findAllByBrandAndDeviceType(
      String brand, String deviceType, String segmentName) {
    DeviceType queryDeviceType = DeviceType.fromString(deviceType).orElse(DeviceType.MOBILE);

    int limit = getQueryLimit(brand, queryDeviceType);
    // Check for Segmentation at Device level, if the module is not segmented at
    // device level then
    // need to send Universal records only
    PageRequest pageRequest =
        PageRequest.of(
            0, getQueryLimit(brand, queryDeviceType), SortableService.SORT_BY_SORT_ORDER_ASC);
    if (!SegmentConstants.UNIVERSAL.equalsIgnoreCase(segmentName)) {
      segmentName =
          segmentedModuleSerive.isSegmentedModule(
                  FooterMenu.class.getSimpleName(), queryDeviceType, brand)
              ? segmentName
              : SegmentConstants.UNIVERSAL;
    }
    List<FooterMenu> footerMenus =
        findByBrandAndSegmentNameAndDeviceTypeAndIsDisableFalse(
            brand, segmentName, Optional.of(queryDeviceType.getValue()), false, pageRequest);

    return CollectionUtils.isEmpty(footerMenus) || footerMenus.size() < limit
        ? footerMenus
        : footerMenus.subList(0, limit);
  }

  private int getQueryLimit(String brand, DeviceType deviceType) {
    int limit = DEFAULT_QUERY_LIMIT;
    if (brand.equals("rcomb") || brand.equals("connect")) {
      limit = RCOMB_CONNECT_QUERY_LIMIT;
    }
    if (deviceType.equals(DeviceType.DESKTOP)) {
      limit = Integer.MAX_VALUE; // return all elements for desktop device
    }
    return limit;
  }

  public Optional<FooterMenu> attachImage(
      FooterMenu menu, @ValidFileType("png") MultipartFile file) {
    return imageEntityService.attachAllSizesImage(menu, file, footerMenuImagePath);
  }

  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId to null delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<FooterMenu> attachSvgImage(
      FooterMenu menu, @ValidFileType("svg") MultipartFile file) {
    return svgEntityService.attachSvgImage(menu, file, footerMenuImagePath.getSvgMenuPath());
  }

  public Optional<FooterMenu> removeImage(FooterMenu menu) {
    return imageEntityService.removeAllSizesImage(menu);
  }

  /**
   * @deprecated use SvgImages api to delete images and use update the menu endpoint to set the
   *     svgId to null delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<FooterMenu> removeSvgImage(FooterMenu menu) {
    return svgEntityService.removeSvgImage(menu);
  }

  @Override
  public void delete(String id) {
    Optional<FooterMenu> point = findOne(id);
    if (point.isPresent()) {
      FooterMenuArchive archive = prepareArchivalEntity(point.get());
      archive.setDeleted(true);
      super.saveArchivalEntity(archive);
      super.delete(id);
    }
  }

  @Override
  public <S extends FooterMenu> S prepareArchivalEntity(FooterMenu entity) {
    return (S) modelMapper.map(entity, FooterMenuArchive.class);
  }

  public List<FooterMenu> findByBrandAndSegmentNameAndDeviceTypeAndIsDisableFalse(
      String brand,
      String segmentName,
      Optional<String> deviceType,
      boolean isDisabled,
      PageRequest pageRequest) {

    return SegmentConstants.UNIVERSAL.equalsIgnoreCase(segmentName)
        ? getUniversal(brand, deviceType, isDisabled, pageRequest)
        : getSegmentAndUniversal(brand, segmentName, deviceType, isDisabled);
  }

  public List<FooterMenu> getUniversal(
      String brand, Optional<String> deviceType, boolean isDisabled, PageRequest pageRequest) {

    return !deviceType.isPresent()
        ? footerMenuRepository.findUniversalRecordsByBrand(brand, isDisabled, pageRequest)
        : footerMenuRepository.findUniversalRecordsByBrand(
            brand, deviceType.get(), isDisabled, pageRequest);
  }

  private List<FooterMenu> getSegmentAndUniversal(
      String brand, String segmentName, Optional<String> deviceType, boolean isDisable) {

    List<FooterMenu> recordsWithSegmentReference =
        super.sortByOrder(
            segmentName, getAllRecordsBySegmentName(brand, segmentName, deviceType, isDisable));

    List<String> inclusiveListIds =
        recordsWithSegmentReference.stream().map(FooterMenu::getId).collect(Collectors.toList());

    List<FooterMenu> universalList =
        findAllUniversalAndNotInsegmentReferences(
            brand, segmentName, inclusiveListIds, deviceType, isDisable);
    recordsWithSegmentReference.addAll(universalList);
    return recordsWithSegmentReference;
  }

  public List<FooterMenu> getAllRecordsBySegmentName(
      String brand, String segmentName, Optional<String> deviceType, boolean isDisabled) {
    return !deviceType.isPresent()
        ? footerMenuRepository.findAllByBrandAndSegmentName(
            brand, Arrays.asList(segmentName), isDisabled)
        : footerMenuRepository.findAllByBrandAndSegmentNameAndDeviceType(
            brand, Arrays.asList(segmentName), deviceType.get(), isDisabled);
  }

  public List<FooterMenu> findAllUniversalAndNotInsegmentReferences(
      String brand,
      String segmentName,
      List<String> inclusiveIds,
      Optional<String> deviceType,
      boolean isDisabled) {

    return !deviceType.isPresent()
        ? findAllUniversalAndNotInsegmentReferences(brand, segmentName, inclusiveIds, isDisabled)
        : findAllUniversalAndNotInsegmentReferences(
            brand, segmentName, inclusiveIds, deviceType.get(), isDisabled);
  }

  private List<FooterMenu> findAllUniversalAndNotInsegmentReferences(
      String brand,
      String segmentName,
      List<String> inclusiveIds,
      String deviceType,
      boolean isDisabled) {
    return footerMenuRepository
        .findByBrandAndDeviceTypeAndApplyUniversalSegmentsAndNotInExclusionListAndInInclusiveList(
            brand,
            Arrays.asList(segmentName),
            inclusiveIds,
            deviceType,
            isDisabled,
            SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  private List<FooterMenu> findAllUniversalAndNotInsegmentReferences(
      String brand, String segmentName, List<String> inclusiveIds, boolean isDisabled) {
    return footerMenuRepository
        .findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
            brand,
            Arrays.asList(segmentName),
            inclusiveIds,
            isDisabled,
            SortableService.SORT_BY_SORT_ORDER_ASC);
  }
}
