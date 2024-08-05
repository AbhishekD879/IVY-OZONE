package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.PopularAccaWidget;

public interface PopularAccaWidgetRepository extends CustomMongoRepository<PopularAccaWidget> {
  boolean existsByBrand(String brand);
}
