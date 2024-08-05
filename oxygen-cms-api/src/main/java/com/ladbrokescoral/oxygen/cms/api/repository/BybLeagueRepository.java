package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.BybLeague;
import java.util.List;

public interface BybLeagueRepository extends CustomMongoRepository<BybLeague> {
  List<BybLeague> findAllByBrandOrderBySortOrderAsc(String brand);
}
