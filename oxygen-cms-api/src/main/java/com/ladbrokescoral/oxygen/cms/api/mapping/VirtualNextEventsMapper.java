package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.VirtualDto;
import com.ladbrokescoral.oxygen.cms.api.dto.VirtualNextEventDto;
import com.ladbrokescoral.oxygen.cms.api.entity.VirtualNextEvent;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface VirtualNextEventsMapper {
  VirtualNextEventsMapper MAPPER = Mappers.getMapper(VirtualNextEventsMapper.class);

  VirtualNextEventDto toDto(VirtualNextEvent virtualNextEvent);

  VirtualNextEvent toEntity(VirtualDto virtualDto);
}
