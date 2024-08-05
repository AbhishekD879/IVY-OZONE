package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSport;
import java.util.List;

public interface VirtualSportRepository extends CustomMongoRepository<VirtualSport> {

  List<VirtualSport> findByBrandAndActiveIsTrueOrderBySortOrderAsc(String brand);
}
