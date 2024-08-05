package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSport;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSportWithTracksRefs;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface VirtualSportWithTracksRefsMapper {
  static VirtualSportWithTracksRefsMapper getInstance() {
    return VirtualSportWithTracksRefsMapper.VirtualSportWithTracksRefsMapperInstance.INSTANCE;
  }

  VirtualSportWithTracksRefs withTrackRefs(VirtualSport entity);

  final class VirtualSportWithTracksRefsMapperInstance {
    private static final VirtualSportWithTracksRefsMapper INSTANCE =
        Mappers.getMapper(VirtualSportWithTracksRefsMapper.class);

    private VirtualSportWithTracksRefsMapperInstance() {}
  }
}
