package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.StatisticContent;
import com.ladbrokescoral.oxygen.cms.api.dto.StatisticContentDto;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface StatisticContentMapper {

  StatisticContentMapper MAPPER = Mappers.getMapper(StatisticContentMapper.class);

  @Mapping(target = "createdBy", ignore = true)
  @Mapping(target = "createdByUserName", ignore = true)
  @Mapping(target = "updatedBy", ignore = true)
  @Mapping(target = "updatedByUserName", ignore = true)
  @Mapping(target = "createdAt", ignore = true)
  @Mapping(target = "updatedAt", ignore = true)
  StatisticContent toEntity(StatisticContentDto dto);

  StatisticContentDto toDto(StatisticContent entity);
}
