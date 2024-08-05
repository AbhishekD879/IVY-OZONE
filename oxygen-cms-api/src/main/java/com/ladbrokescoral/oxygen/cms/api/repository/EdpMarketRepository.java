package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.EdpMarket;
import java.util.List;

public interface EdpMarketRepository extends CustomMongoRepository<EdpMarket> {
  List<EdpMarket> findAllByBrandOrderBySortOrderAsc(String brand);

  List<EdpMarket> findByLastItemIsTrueAndIdNot(String id);
}
