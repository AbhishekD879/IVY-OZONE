package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.StaticTextOtf;

public interface StaticTextOtfRepository extends CustomMongoRepository<StaticTextOtf> {
  boolean existsByPageNameAndEnabledIsTrueAndIdNotAndBrandIs(
      String pageName, String id, String brand);
}
