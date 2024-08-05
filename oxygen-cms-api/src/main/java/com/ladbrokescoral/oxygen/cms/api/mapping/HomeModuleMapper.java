package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.DataSelectionDto;
import com.ladbrokescoral.oxygen.cms.api.dto.DeviceDto;
import com.ladbrokescoral.oxygen.cms.api.dto.EventsSelectionSettingDto;
import com.ladbrokescoral.oxygen.cms.api.dto.HomeModuleDto;
import com.ladbrokescoral.oxygen.cms.api.dto.HomeModuleSegmentedDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventDto;
import com.ladbrokescoral.oxygen.cms.api.entity.DataSelection;
import com.ladbrokescoral.oxygen.cms.api.entity.Device;
import com.ladbrokescoral.oxygen.cms.api.entity.EventsSelectionSetting;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModuleData;
import com.ladbrokescoral.oxygen.cms.api.entity.Visibility;
import java.time.Duration;
import java.util.List;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface HomeModuleMapper extends SegmentReferenceMapper {
  HomeModuleMapper INSTANCE = Mappers.getMapper(HomeModuleMapper.class);

  @Mapping(
      target = "showEventsForDays",
      expression = "java(getShowEventsForDays(source.getVisibility()))")
  HomeModuleDto toDto(HomeModule source);

  DeviceDto toDto(Device source);

  EventsSelectionSettingDto toDto(EventsSelectionSetting source);

  DataSelectionDto toDto(DataSelection source);

  HomeModuleData toHomeModuleData(SiteServeEventDto source);

  default long getShowEventsForDays(Visibility visibility) {
    return Duration.between(visibility.getDisplayFrom(), visibility.getDisplayTo()).toDays();
  }

  @Mapping(target = "segmentReferences", ignore = true)
  @Mapping(target = "segments", ignore = true)
  HomeModuleSegmentedDto toSegmentedDto(HomeModule entity);

  default HomeModuleSegmentedDto toSegmentedDto(HomeModule entity, List<String> segments) {
    HomeModuleSegmentedDto homeModuleSegmentedDto = toSegmentedDto(entity);
    homeModuleSegmentedDto.setSegments(getSegments(entity, segments));
    homeModuleSegmentedDto.setSegmentReferences(getSegmentReferences(entity));
    return homeModuleSegmentedDto;
  }
}
