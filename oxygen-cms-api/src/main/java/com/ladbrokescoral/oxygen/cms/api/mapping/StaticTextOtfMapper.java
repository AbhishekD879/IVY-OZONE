package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.StaticTextOtfDto;
import com.ladbrokescoral.oxygen.cms.api.entity.StaticTextOtf;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface StaticTextOtfMapper {
  StaticTextOtfMapper INSTANCE = Mappers.getMapper(StaticTextOtfMapper.class);

  StaticTextOtfDto toDto(StaticTextOtf staticText);
}
