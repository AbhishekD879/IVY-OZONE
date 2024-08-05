package com.ladbrokescoral.oxygen.cms.api.controller.mapping;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.EventHubControllerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.EventHub;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface EventHubControllerMapper {

  EventHubControllerMapper INSTANCE = Mappers.getMapper(EventHubControllerMapper.class);

  @Mapping(target = "createdBy", ignore = true)
  @Mapping(target = "createdByUserName", ignore = true)
  @Mapping(target = "updatedBy", ignore = true)
  @Mapping(target = "updatedByUserName", ignore = true)
  @Mapping(target = "createdAt", ignore = true)
  @Mapping(target = "updatedAt", ignore = true)
  @Mapping(target = "sortOrder", ignore = true)
  EventHub toEntity(EventHubControllerDto entity);
}
