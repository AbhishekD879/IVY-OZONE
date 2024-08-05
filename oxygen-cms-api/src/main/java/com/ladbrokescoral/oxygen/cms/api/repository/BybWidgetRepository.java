package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.BybWidget;

public interface BybWidgetRepository extends CustomMongoRepository<BybWidget> {
  boolean existsByBrand(String brand);
}
