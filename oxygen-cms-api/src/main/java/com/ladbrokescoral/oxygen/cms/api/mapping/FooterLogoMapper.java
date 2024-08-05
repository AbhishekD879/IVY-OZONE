package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.FooterLogoDto;
import com.ladbrokescoral.oxygen.cms.api.dto.FooterLogoNativeDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterLogo;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface FooterLogoMapper {
  FooterLogoMapper INSTANCE = Mappers.getMapper(FooterLogoMapper.class);

  FooterLogoNativeDto toDtoNative(FooterLogo entity);

  FooterLogoDto toDto(FooterLogo entity);
}
