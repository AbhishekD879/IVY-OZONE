package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.League;
import java.util.List;

public interface LeaguesRepository extends CustomMongoRepository<League> {
  List<League> findAllByBrandOrderBySortOrderAsc(String brand);
}
