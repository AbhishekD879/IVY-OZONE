package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.YourCallLeague;
import java.util.List;

public interface YourCallLeagueRepository extends CustomMongoRepository<YourCallLeague> {
  List<YourCallLeague> findAllByBrandOrderBySortOrderAsc(String brand);

  List<YourCallLeague> findAllByBrandAndEnabledFalse(String brand);

  List<YourCallLeague> findAllByBrandAndTypeId(String brand, Integer typeId);
}
