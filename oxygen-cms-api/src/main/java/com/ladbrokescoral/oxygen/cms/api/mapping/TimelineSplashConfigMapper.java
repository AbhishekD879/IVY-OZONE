package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.TimelineSplashConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineSplashConfig;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface TimelineSplashConfigMapper {
  TimelineSplashConfigMapper INSTANCE = Mappers.getMapper(TimelineSplashConfigMapper.class);

  TimelineSplashConfigDto toDto(TimelineSplashConfig entity);
}
