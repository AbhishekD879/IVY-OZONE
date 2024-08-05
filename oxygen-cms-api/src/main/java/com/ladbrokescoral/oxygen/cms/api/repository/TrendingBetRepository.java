package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.TrendingBet;
import java.util.Optional;

public interface TrendingBetRepository extends CustomMongoRepository<TrendingBet> {
  Optional<TrendingBet> findTrendingBetByBrandAndType(String brand, String type);
}
