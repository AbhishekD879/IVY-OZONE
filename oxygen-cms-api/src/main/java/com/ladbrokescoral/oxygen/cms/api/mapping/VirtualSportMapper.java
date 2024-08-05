package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSport;
import com.ladbrokescoral.oxygen.cms.api.dto.VirtualSportDto;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface VirtualSportMapper {
  static VirtualSportMapper getInstance() {
    return VirtualSportMapper.VirtualSportMapperInstance.INSTANCE;
  }

  VirtualSportDto toDto(VirtualSport entity);

  final class VirtualSportMapperInstance {
    private static final VirtualSportMapper INSTANCE = Mappers.getMapper(VirtualSportMapper.class);

    private VirtualSportMapperInstance() {}
  }
}
