package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.SsoPageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SsoPage;
import org.mapstruct.AfterMapping;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.mapstruct.factory.Mappers;

@Mapper
public interface SsoPageMapper {

  SsoPageMapper INSTANCE = Mappers.getMapper(SsoPageMapper.class);

  @Mapping(target = "target", ignore = true)
  SsoPageDto toDto(SsoPage entity, String osType);

  @AfterMapping
  default void setTarget(String osType, SsoPage entity, @MappingTarget SsoPageDto ssoPageDto) {
    if (osType.equals("ios")) {
      ssoPageDto.setTarget(entity.getTargetIOS());
    }
    if (osType.equals("android")) {
      ssoPageDto.setTarget(entity.getTargetAndroid());
    }
  }
}
