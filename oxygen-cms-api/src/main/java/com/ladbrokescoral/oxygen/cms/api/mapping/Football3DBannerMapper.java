package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.FootballBanner3dDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Football3DBanner;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {DateMapper.class})
public interface Football3DBannerMapper {
  Football3DBannerMapper INSTANCE = Mappers.getMapper(Football3DBannerMapper.class);

  FootballBanner3dDto toDto(Football3DBanner entity);
}
