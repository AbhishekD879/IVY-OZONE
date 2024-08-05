package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.InplayStatsSorting;
import java.util.List;

public interface InplayStatsSortingRepository extends CustomMongoRepository<InplayStatsSorting> {

  List<InplayStatsSorting> findAllByBrandAndCategoryIdOrderBySortOrderAsc(
      String brand, Integer categoryId);
}
