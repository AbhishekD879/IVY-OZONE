package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.CouponMarketSelector;

public interface CouponMarketSelectorRepository
    extends CustomMongoRepository<CouponMarketSelector> {
  boolean existsByTemplateMarketNameAndIdNotAndBrandIs(
      String templateMarketName, String id, String brand);
}
