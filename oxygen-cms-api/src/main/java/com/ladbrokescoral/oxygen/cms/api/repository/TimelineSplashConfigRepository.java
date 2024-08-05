package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineSplashConfig;
import java.util.Optional;

public interface TimelineSplashConfigRepository
    extends CustomMongoRepository<TimelineSplashConfig> {
  Optional<TimelineSplashConfig> findOneByBrand(String brand);

  boolean existsByBrand(String brand);
}
