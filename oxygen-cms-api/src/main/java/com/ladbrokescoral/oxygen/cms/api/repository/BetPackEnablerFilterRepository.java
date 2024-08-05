package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackFilter;
import java.util.List;

public interface BetPackEnablerFilterRepository extends CustomMongoRepository<BetPackFilter> {
  List<BetPackFilter> findByBrandAndFilterActiveTrue(String brand);

  Long deleteByFilterName(String filterName);
}
