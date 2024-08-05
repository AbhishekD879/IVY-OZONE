package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.InplayStatsDisplay;
import java.util.List;

public interface InplayStatsDisplayRepository extends CustomMongoRepository<InplayStatsDisplay> {
  List<InplayStatsDisplay> findAllByBrandAndCategoryIdOrderBySortOrderAsc(
      String brand, Integer categoryId);
}
