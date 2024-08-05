package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Config;
import java.util.Optional;

public interface TimelineConfigRepository extends CustomMongoRepository<Config> {
  Optional<Config> findOneByBrand(String brand);

  boolean existsByBrand(String brand);
}
