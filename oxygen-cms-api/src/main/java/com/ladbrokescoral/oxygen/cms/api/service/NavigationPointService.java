package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.NavigationPointArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.NavigationPointArchive;
import com.ladbrokescoral.oxygen.cms.api.dto.AutomaticUpdateDto;
import com.ladbrokescoral.oxygen.cms.api.dto.NavigationPointDto;
import com.ladbrokescoral.oxygen.cms.api.dto.NavigationPointSegmentedDto;
import com.ladbrokescoral.oxygen.cms.api.entity.DeviceType;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.mapping.NavigationPointMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.NavigationPointRepository;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

@Service
public class NavigationPointService extends AbstractSegmentService<NavigationPoint> {

  private static final String PREFIX = "SB:";
  private ModelMapper modelMapper;
  private SegmentedModuleSerive segmentedModuleSerive;
  protected NavigationPointRepository navigationPointRepository;

  private AutomaticUpdateService automaticUpdateService;

  @Autowired
  public NavigationPointService(
      NavigationPointRepository navigationPointRepository,
      NavigationPointArchivalRepository navigationPointArchivalRepository,
      ModelMapper modelMapper,
      SegmentService segmentService,
      SegmentedModuleSerive segmentedModuleSerive,
      AutomaticUpdateService automaticUpdateService) {
    super(navigationPointRepository, navigationPointArchivalRepository, segmentService);
    this.modelMapper = modelMapper;
    this.segmentedModuleSerive = segmentedModuleSerive;
    this.navigationPointRepository = navigationPointRepository;
    this.automaticUpdateService = automaticUpdateService;
  }

  public List<NavigationPointSegmentedDto> findAllActiveByBrand(String brand) {
    PageRequest pageRequest =
        PageRequest.of(0, Integer.MAX_VALUE, SortableService.SORT_BY_SORT_ORDER_ASC);
    List<NavigationPoint> navigationPoints =
        navigationPointRepository.findAllActiveRecordsByBrand(brand, pageRequest);
    List<String> segments = segmentService.getSegmentsForSegmentedViews(brand);
    return navigationPoints.stream()
        .map(e -> NavigationPointMapper.INSTANCE.toSegmentedDto(e, segments))
        .collect(Collectors.toList());
  }

  public List<NavigationPointDto> getNavigationPointByBrandEnabled(String brand) {
    return findByBrandAndSegmentName(brand, SegmentConstants.UNIVERSAL).stream()
        .filter(NavigationPoint::isEnabled)
        .map(e -> modelMapper.map(e, NavigationPointDto.class))
        .collect(Collectors.toList());
  }

  public List<NavigationPointDto> getNavigationPointByBrandEnabled(
      String brand, String segmentName, DeviceType deviceType) {
    // Check for Segmentation at Device level, if the module is not segmented at
    // device level then
    // need to send Universal records only
    if (!SegmentConstants.UNIVERSAL.equals(segmentName)) {
      segmentName =
          segmentedModuleSerive.isSegmentedModule(
                  NavigationPoint.class.getSimpleName(), deviceType, brand)
              ? segmentName
              : SegmentConstants.UNIVERSAL;
    }
    return findByBrandAndSegmentName(brand, segmentName).stream()
        .filter(NavigationPoint::isEnabled)
        .map(e -> modelMapper.map(e, NavigationPointDto.class))
        .collect(Collectors.toList());
  }

  @Override
  public NavigationPointArchive prepareArchivalEntity(NavigationPoint entity) {
    return modelMapper.map(entity, NavigationPointArchive.class);
  }

  @Override
  public void delete(String id) {
    Optional<NavigationPoint> point = findOne(id);
    if (point.isPresent()) {
      NavigationPointArchive archive = prepareArchivalEntity(point.get());
      archive.setDeleted(true);
      super.saveArchivalEntity(archive);
      super.delete(id);
    }
  }

  @Override
  public NavigationPoint update(NavigationPoint existingEntity, NavigationPoint updateEntity) {
    if (!updateEntity.getTitle().equalsIgnoreCase(existingEntity.getTitle())) {
      AutomaticUpdateDto automaticUpdateDto = new AutomaticUpdateDto();
      automaticUpdateDto.setId(updateEntity.getId());
      automaticUpdateDto.setBrand(updateEntity.getBrand());
      automaticUpdateDto.setUpdatedTitle(PREFIX + updateEntity.getTitle());
      this.automaticUpdateService.doUpdate(automaticUpdateDto);
    }
    return super.update(existingEntity, updateEntity);
  }
}
