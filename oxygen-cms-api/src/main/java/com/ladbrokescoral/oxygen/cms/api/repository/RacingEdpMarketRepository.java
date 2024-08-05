package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.RacingEdpMarket;
import java.util.List;

public interface RacingEdpMarketRepository extends CustomMongoRepository<RacingEdpMarket> {

  List<RacingEdpMarket> findByName(String name);

  List<RacingEdpMarket> findAllByBrandOrderBySortOrderAsc(String brand);
}
