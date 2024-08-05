package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.AssetManagementDto;
import com.ladbrokescoral.oxygen.cms.api.entity.AssetManagement;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface AssetManagementMapper {
  AssetManagementMapper INSTANCE = Mappers.getMapper(AssetManagementMapper.class);

  AssetManagementDto toDto(AssetManagement entity);
}
