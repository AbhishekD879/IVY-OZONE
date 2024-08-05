package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.ModuleRibbonTabDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ModuleRibbonTabSegmentedDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ModuleRibbonTab;
import java.util.List;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface ModuleRibbonTabMapper extends SegmentReferenceMapper {

  ModuleRibbonTabMapper INSTANCE = Mappers.getMapper(ModuleRibbonTabMapper.class);

  ModuleRibbonTabDto toDto(ModuleRibbonTab entity);

  @Mapping(target = "segmentReferences", ignore = true)
  @Mapping(target = "segments", ignore = true)
  ModuleRibbonTabSegmentedDto toSegmentedDto(ModuleRibbonTab entity);

  default ModuleRibbonTabSegmentedDto toSegmentedDto(
      ModuleRibbonTab entity, List<String> segments) {
    ModuleRibbonTabSegmentedDto moduleRibbonTabSegmentedDto = toSegmentedDto(entity);
    moduleRibbonTabSegmentedDto.setSegments(getSegments(entity, segments));
    moduleRibbonTabSegmentedDto.setSegmentReferences(getSegmentReferences(entity));
    return moduleRibbonTabSegmentedDto;
  }
}
