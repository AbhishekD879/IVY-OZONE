package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.ModularContentDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ModuleDataDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ModuleDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SegmentReferenceDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Device;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModuleData;
import com.ladbrokescoral.oxygen.cms.api.entity.ModuleRibbonTab;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.mapping.ModularContentMapUtil.MapDevices;
import com.ladbrokescoral.oxygen.cms.api.mapping.ModularContentMapUtil.ModularContentUtils;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import org.mapstruct.AfterMapping;
import org.mapstruct.BeforeMapping;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.springframework.util.CollectionUtils;

@Mapper(uses = {ModularContentMapUtil.class, DateMapper.class})
public abstract class ModularContentMapper {

  @Mapping(target = "id", source = "internalId")
  @Mapping(target = "moduleDtos", expression = "java(new java.util.ArrayList<>())")
  @Mapping(
      target = "devices",
      qualifiedBy = {ModularContentUtils.class, MapDevices.class})
  public abstract ModularContentDto toDto(ModuleRibbonTab entity);

  @Mapping(target = "publishedDevices", ignore = true)
  @Mapping(target = "category", ignore = true)
  @Mapping(target = "version", source = "entity.ver")
  @Mapping(target = "displayOrder", source = "entity.sortOrder")
  public abstract ModuleDto toDto(HomeModule entity, String brand);

  @Mapping(target = "marketsCount", source = "marketCount")
  @Mapping(target = "marketId", ignore = true)
  @Mapping(target = "outcomeId", ignore = true)
  @Mapping(target = "outcomeStatus", ignore = true)
  public abstract ModuleDataDto toDto(HomeModuleData entity);

  @BeforeMapping
  protected void stopIfEmptyData(HomeModule entity) {
    if (CollectionUtils.isEmpty(entity.getData())
        && !entity.getDataSelection().getSelectionType().equals("RacingGrid")) {
      entity = null;
    }
  }

  @AfterMapping
  protected void setPublishedDevices(
      String brand, HomeModule entity, @MappingTarget ModuleDto moduleDto) {
    if (Objects.isNull(entity.getPublishedDevices())
        || Objects.isNull(entity.getPublishedDevices().get(brand))) {
      moduleDto.setPublishedDevices(Arrays.asList("desktop", "mobile", "tablet"));
    } else {
      Device device = entity.getPublishedDevices().get(brand);
      if (device.isDesktop()) moduleDto.getPublishedDevices().add("desktop");
      if (device.isMobile()) moduleDto.getPublishedDevices().add("mobile");
      if (device.isTablet()) moduleDto.getPublishedDevices().add("tablet");
    }
  }

  public ModuleDto toDto(HomeModule homeModule, String brand, List<String> segments) {
    ModuleDto moduleDto = toDto(homeModule, brand);
    moduleDto.setSegments(getSegments(homeModule, segments));
    moduleDto.setSegmentReferences(getSegmentReferences(homeModule));
    return moduleDto;
  }

  private List<String> getSegments(HomeModule homeModule, List<String> segments) {
    if (homeModule.isUniversalSegment()) {
      if (!CollectionUtils.isEmpty(homeModule.getExclusionList())) {
        return segments.stream()
            .filter(seg -> !homeModule.getExclusionList().contains(seg))
            .collect(Collectors.toList());
      }
      return segments;
    } else {
      return homeModule.getInclusionList();
    }
  }

  private List<SegmentReferenceDto> getSegmentReferences(HomeModule homeModule) {
    List<SegmentReferenceDto> segmentReferences = new ArrayList<>();
    if (!CollectionUtils.isEmpty(homeModule.getSegmentReferences())) {
      homeModule
          .getSegmentReferences()
          .forEach(
              (SegmentReference segRef) -> {
                SegmentReferenceDto segmentReference = toDto(segRef);
                segmentReferences.add(segmentReference);
              });
    }
    return segmentReferences;
  }

  @Mapping(target = "segment", source = "segmentName")
  @Mapping(target = "displayOrder", source = "sortOrder")
  public abstract SegmentReferenceDto toDto(SegmentReference entity);
}
