package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.SportsFeaturedTab;

public interface SportsFeaturedTabRepository extends CustomMongoRepository<SportsFeaturedTab> {
  SportsFeaturedTab findByBrandIgnoreCaseAndPathIgnoreCaseAndDisabledIsFalse(
      String brand, String path);
}
