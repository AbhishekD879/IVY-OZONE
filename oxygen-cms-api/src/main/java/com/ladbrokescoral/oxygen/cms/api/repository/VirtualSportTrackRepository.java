package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSportTrack;
import java.util.List;

public interface VirtualSportTrackRepository extends CustomMongoRepository<VirtualSportTrack> {
  List<VirtualSportTrack> findBySportIdOrderBySortOrderAsc(String sportId);

  List<VirtualSportTrack> findBySportIdAndActiveIsTrueOrderBySortOrderAsc(String sportId);
}
