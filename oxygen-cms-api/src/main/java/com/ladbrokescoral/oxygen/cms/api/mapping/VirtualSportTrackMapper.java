package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSportTrack;
import com.ladbrokescoral.oxygen.cms.api.dto.VirtualSportTrackDto;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface VirtualSportTrackMapper {
  static VirtualSportTrackMapper getInstance() {
    return VirtualSportTrackMapper.VirtualSportTrackMapperInstance.INSTANCE;
  }

  VirtualSportTrackDto toDto(VirtualSportTrack entity);

  final class VirtualSportTrackMapperInstance {
    private static final VirtualSportTrackMapper INSTANCE =
        Mappers.getMapper(VirtualSportTrackMapper.class);

    private VirtualSportTrackMapperInstance() {}
  }
}
