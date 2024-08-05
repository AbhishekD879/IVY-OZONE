package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.NavigationPointArchive;
import com.ladbrokescoral.oxygen.cms.api.dto.NavigationPointDto;
import com.ladbrokescoral.oxygen.cms.api.dto.NavigationPointSegmentedDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import java.util.List;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface NavigationPointMapper extends SegmentReferenceMapper {
  NavigationPointMapper INSTANCE = Mappers.getMapper(NavigationPointMapper.class);

  NavigationPointDto toDto(NavigationPoint entity);

  @Mapping(target = "segmentReferences", ignore = true)
  @Mapping(target = "segments", ignore = true)
  NavigationPointSegmentedDto toSegmentedDto(NavigationPoint entity);

  NavigationPointArchive toArchivalEntity(NavigationPoint entity);

  default NavigationPointSegmentedDto toSegmentedDto(
      NavigationPoint entity, List<String> segments) {
    NavigationPointSegmentedDto navigationPointSegmentedDto = toSegmentedDto(entity);
    navigationPointSegmentedDto.setSegments(getSegments(entity, segments));
    navigationPointSegmentedDto.setSegmentReferences(getSegmentReferences(entity));
    return navigationPointSegmentedDto;
  }
}
