package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.InplayStatsSortingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.InplayStatsSorting;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface InplayStatsSortingMapper {

  InplayStatsSortingMapper MAPPER = Mappers.getMapper(InplayStatsSortingMapper.class);

  InplayStatsSorting toEntity(InplayStatsSortingDto dto);

  InplayStatsSortingDto toDto(InplayStatsSorting entity);
}
