package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.MaintenancePageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.MaintenancePage;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper(uses = DateMapper.class)
public interface MaintenancePageMapper {
  MaintenancePageMapper INSTANCE = Mappers.getMapper(MaintenancePageMapper.class);

  MaintenancePageDto toDto(MaintenancePage entity);
}
