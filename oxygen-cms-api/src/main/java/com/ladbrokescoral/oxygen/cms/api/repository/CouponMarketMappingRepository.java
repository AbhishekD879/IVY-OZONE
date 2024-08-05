package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.CouponMarketMappingEntity;
import java.util.Optional;
import org.springframework.data.mongodb.repository.Query;

public interface CouponMarketMappingRepository
    extends CustomMongoRepository<CouponMarketMappingEntity> {

  @Query("{'couponId': ?0}")
  Optional<CouponMarketMappingEntity> findByCouponId(String couponId);
}
