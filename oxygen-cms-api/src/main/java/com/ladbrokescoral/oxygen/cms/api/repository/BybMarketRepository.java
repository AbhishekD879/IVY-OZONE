package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.BybMarket;
import java.util.List;

public interface BybMarketRepository extends CustomMongoRepository<BybMarket> {
  List<BybMarket> findAllByBrandOrderBySortOrderAsc(String brand);
}
