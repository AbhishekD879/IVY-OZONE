package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.StatisticContent;
import com.ladbrokescoral.oxygen.cms.api.entity.MarketType;
import java.util.List;
import java.util.Optional;

public interface StatisticContentRepository extends CustomMongoRepository<StatisticContent> {

  Optional<List<StatisticContent>> findByBrandAndEventIdAndMarketIdAndMarketType(
      String brand, String eventId, String marketId, MarketType marketType);

  Optional<StatisticContent> findByIdAndBrand(String id, String brand);

  List<StatisticContent> findByEventId(String eventId);

  List<StatisticContent> findAllByBrandAndEventIdOrderBySortOrderAsc(String brand, String eventId);
}
