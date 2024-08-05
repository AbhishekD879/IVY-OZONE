package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.SeoAutoInitDataDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoAutoPage;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;
import org.springframework.stereotype.Component;

@Mapper
@Component
public interface SeoAutoInitDataDtoMapper {

  SeoAutoInitDataDtoMapper INSTANCE = Mappers.getMapper(SeoAutoInitDataDtoMapper.class);

  SeoAutoInitDataDto toInitDataDto(SeoAutoPage entity);
}
