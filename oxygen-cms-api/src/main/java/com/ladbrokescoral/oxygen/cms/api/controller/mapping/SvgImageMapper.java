package com.ladbrokescoral.oxygen.cms.api.controller.mapping;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.SvgImageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgImage;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface SvgImageMapper {

  SvgImageMapper INSTANCE = Mappers.getMapper(SvgImageMapper.class);

  SvgImage toEntity(SvgImageDto entity);

  SvgImageDto toDto(SvgImage entity);
}
