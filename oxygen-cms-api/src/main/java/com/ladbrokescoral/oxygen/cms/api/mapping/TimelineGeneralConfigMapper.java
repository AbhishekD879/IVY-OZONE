package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.TimelineGeneralConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Config;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface TimelineGeneralConfigMapper {
  TimelineGeneralConfigMapper INSTANCE = Mappers.getMapper(TimelineGeneralConfigMapper.class);

  TimelineGeneralConfigDto toDto(Config entity);
}
