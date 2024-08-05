package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.InplayStatsDisplayDto;
import com.ladbrokescoral.oxygen.cms.api.entity.InplayStatsDisplay;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface InplayStatsDisplayMapper {

  InplayStatsDisplayMapper MAPPER = Mappers.getMapper(InplayStatsDisplayMapper.class);

  InplayStatsDisplay toEntity(InplayStatsDisplayDto dto);

  InplayStatsDisplayDto toDto(InplayStatsDisplay entity);
}
